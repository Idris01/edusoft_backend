from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from backend.models import University, Language, AppUser, ActivationToken
from cities_light.models import Country, City
from .serializers import (
        UniversitySerializer, 
        UserSerializer,
        EdusoftObtainTokenPairSerializer)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from django.contrib.auth.models import AnonymousUser
from .permissions import IsAdminOrReadOnly, IsAdminReadOnly
from django.conf import settings
import re
from rest_framework_simplejwt.views import TokenObtainPairView
import json


class VerifyAccountAPIView(APIView):
    def get(self, request, *args, **kwargs):

        activation_token = ActivationToken.objects.filter(token=self.kwargs.get("token"))
        if not activation_token:
            return Response(
                    {"detail":"Invalid Token"},
                    status=status.HTTP_400_BAD_REQUEST)
        activated_user = activation_token[0].user
        activated_user.is_active = True
        activated_user.save()
        activation_token.delete()
        return Response(
                {"detail":"Account successfully activated"},
                status=status.HTTP_200_OK)

class EdusoftTokenObtainPairView(TokenObtainPairView):
    serializer_class = EdusoftObtainTokenPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
           user = AppUser.objects.get(email=request.data.get("email"))
           response.data['username'] = user.username
           response.data['email'] = user.email
           ref_sec = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME').total_seconds()
           acc_sec = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME').total_seconds()
           response.data["refresh_expires_seconds"] = ref_sec
           response.data["access_expires_seconds"] = acc_sec
        return response


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = AppUser.objects.all()
    permission_classes = [IsAdminReadOnly]
    required_fields = [
            "username", "password","first_name",
            "confirm_password", "email", "last_name"]

    def post(self, request, *args, **kwargs):

        data = dict(request.data)
        user_data = {
                item:data.get(item,[None])[0]  for item in self.required_fields}

        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")

        for key, value in user_data.items():
            if not value:
                return Response(
                        {key : ["This field is reqired"]},
                        status=status.HTTP_400_BAD_REQUEST)
        
        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                return Response(
                    dict(password=["password mismatch"]),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            elif len(password) < settings.MINIMUM_PASSWORD_SIZE:
                return Response(
                    dict(password=["password too short"]),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif re.search(r"[\s]+", password):
                return Response(
                    dict(password=["password must not include space"]),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            elif not all(
                (
                    re.search("[a-z]+", password),
                    re.search("[A-Z]+", password),
                    re.search("[^a-zA-z0-9]+", password),
                    re.search("[0-9]+", password),
                )
            ):
                return Response(
                    dict(
                        password=[
                            " ".join(
                                (
                                    "password must have lower",
                                    "and uppercase, number and special char",
                                )
                            )
                        ]
                    ),
                    status=status.HTTP_400_BAD_REQUEST)
        serialized_data = self.serializer_class(
                data=user_data)
        
        del user_data["confirm_password"] # remove confirmation data
        user_data["is_active"] = False
        if serialized_data.is_valid():
            new_user = AppUser.objects.create_user(
                    **user_data)
            act_token = ActivationToken.objects.create(user=new_user)
            return Response(
                    dict(
                    message="registration successfull",
                    token=str(act_token.token)),
                    status=status.HTTP_201_CREATED)

        return Response(
                serialized_data.errors,
                status=status.HTTP_400_BAD_REQUEST)


class UniversityDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    lookup_field = "id"
    serializer_class = UniversitySerializer
    permission_classes = [IsAdminOrReadOnly]

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)

        data = dict(request.data)
        data_keys = list(data.keys())
        if response.status_code > 299:
            return response

        uni = University.objects.get(id=kwargs.get(self.lookup_field))

        if "languages" in data_keys and data["languages"]:
            lang_list = []
            for lang in data["languages"]:
                lan, created = Language.objects.get_or_create(name=lang.title())
                lang_list.append(lan)
            uni.languages.set(lang_list)
            uni.save()
        if "country" in data_keys and data["country"]:
            country = data["country"][0]
            country = Country.objects.filter(code2__iexact=country)
            if country:
                country = country[0]
                uni.country = country
                uni.save()
        if "city" in data_keys and data["city"]:
            city = City.objects.filter(country=uni.country, name=data["city"][0])
            if city:
                uni.city = city[0]
                uni.save()
        return Response(self.serializer_class(uni).data, status=response.status_code)


class UniversityListCreateAPIView(ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["$department__course__name"]

    def post(self, request, *args, **kwargs):
        data = {key: ",".join(value) for key, value in dict(request.data).items()}
        errors = {}

        # check the required permission
        if isinstance(request.user, AnonymousUser) or not request.user.is_superuser:
            return Response(
                dict(message="Permission denied"), status=status.HTTP_401_UNAUTHORIZED
            )

        country_name = ""
        if "country" in data:
            country_code = data.get("country")
            country = Country.objects.filter(code2__iexact=country_code)
            if country:
                country = country[0]
                country_name = country.name
                data["country"] = country.id
            else:
                errors["country"] = "Unknown country {}".format(data["country"])
        if "country" in data and "city" in data:
            city = City.objects.filter(
                country__name=country_name, name__iexact=data.get("city")
            )
            if city:
                data["city"] = city[0].id
            else:
                errors["city"] = "city {} not found in {}".format(
                    data.get("city"), country_name
                )

        if "languages" in data:
            language_list = []
            for language in data.get("languages").split(","):
                try:
                    lang = Language.objects.get(name__iexact=language)
                    if not lang:
                        lang = Language.objects.create(name=language)
                        lang.save()
                    language_list.append(lang.id)
                except Exception:
                    pass
            if language_list:
                data["languages"] = language_list
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        new_university = UniversitySerializer(data=data)

        if new_university.is_valid():
            new_university.save(created_by=request.user)  # add the creator
            return Response(new_university.data, status=status.HTTP_201_CREATED)
        return Response(new_university.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from backend.models import University, Language, Profile, AppUser, ActivationToken, Course
from cities_light.models import Country, City
from .serializers import (
    UniversitySerializer,
    CourseListSerializer,
    UserSerializer,
    ProfileSerializer,
    EdusoftObtainTokenPairSerializer,
    CourseNameSerializer,
    CountryNameSerializer,
    CourseDetailSerializer,
)
from .validators import validate_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, filters
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import make_password
from .permissions import IsAdminOrReadOnly, IsAdminReadOnly
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
import os
from datetime import datetime

# define search filelds based on environment
if os.getenv("ENVIRONMENT") == "Test":
    course_search_fields = ["$name"]
    university_list_search_field = ["$department__course__name"]
else:
    course_search_fields = ["@name"]
    university_list_search_field = ["@department__course__name"]


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(request.user).data
        return Response(serialized_data, status=status.HTTP_200_OK)


class CourseDetailAPIView(RetrieveAPIView):
    serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    lookup_field = "id"


class OptionAPIView(APIView):
    """Define an view of options of Course, and Country available"""

    def get(self, request, *args, **kwargs):
        country_names = CountryNameSerializer(Country.objects.all(), many=True).data
        course_names = CourseNameSerializer(Course.objects.all(), many=True).data
        return Response(
            dict(countries=country_names, courses=course_names), status=status.HTTP_200_OK
        )


class CourseListAPIView(ListAPIView):
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = course_search_fields

    def get_queryset(self):
        country_param = self.request.query_params.get("country")
        search_param = self.request.query_params.get("search")
        course_param = self.request.query_params.get("course")
        query_result = self.queryset
        if country_param:
            query_result = query_result.filter(
                department__university__country__code2__iexact=country_param
            )
        if course_param and not search_param:
            query_result = query_result.filter(name__iexact=course_param)

        return query_result


class UserProfileAPIView(APIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    profile_fields = ["date_of_birth", "gender", "address", "nationality"]

    def get(self, request, *args, **kwargs):
        profile, is_new = Profile.objects.get_or_create(user=request.user)
        serialized_profile = ProfileSerializer(profile)
        return Response(serialized_profile.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        profile, is_new = Profile.objects.get_or_create(user=request.user)
        new_data = {key: value[0] for key, value in dict(request.data).items()}
        error_data = {}
        profile_old = profile.__dict__

        for field in self.profile_fields:
            old = profile_old.get(field)
            new = new_data.get(field)
            if (old is None) and (new is None):
                error_data[field] = "Field is required"
        if error_data:
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        serialized_data = ProfileSerializer(profile, data=new_data)
        if serialized_data.is_valid():
            serialized_data.save(update=True)
            return Response(serialized_data.data, status=status.HTTP_200_OK)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(APIView):
    """Handle user password reset"""

    def get(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"detail": "email required"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = AppUser.objects.filter(email=email)

        if not user:
            return Response(
                {"detail": "account not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = user[0]

        if not user.is_active:
            return Response(
                {"detail": "please validate account"}, status=status.HTTP_400_BAD_REQUEST
            )
        # create a reset token
        reset_token = ActivationToken.objects.create(user=user, category="reset")
        return Response(
            dict(reset_token=str(reset_token.token)), status=status.HTTP_200_OK
        )


class VerifyAccountAPIView(APIView):
    def get(self, request, *args, **kwargs):

        activation_token = ActivationToken.objects.filter(token=self.kwargs.get("token"))
        if not activation_token:
            return Response(
                {"detail": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST
            )
        activated_user = activation_token[0].user
        activated_user.is_active = True
        activated_user.save()
        activation_token.delete()
        return Response(
            {"detail": "Account successfully activated"}, status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        reset_token = ActivationToken.objects.filter(token=self.kwargs.get("token"))
        if not reset_token:
            return Response({"detail": "invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        has_error = validate_password(password, confirm_password)

        if has_error:
            info, stat = has_error
            return Response(info, stat)
        new_passwd = make_password(password)
        user = reset_token[0].user
        user.password = new_passwd
        user.save()
        reset_token[0].delete()

        return Response(
            {"detail": "password reset successfull"}, status=status.HTTP_200_OK
        )


class EdusoftTokenObtainPairView(TokenObtainPairView):
    serializer_class = EdusoftObtainTokenPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = AppUser.objects.get(email=request.data.get("email"))
            response.data["username"] = user.username
            response.data["email"] = user.email
            response.data["first_name"] = user.first_name
            response.data["last_name"] = user.last_name

            ref_sec = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds()
            acc_sec = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds()

            now = datetime.now().timestamp()
            response.data["refresh_expires_seconds"] = int((ref_sec * 1000) + now)
            response.data["access_expires_seconds"] = int((acc_sec * 1000) + now)
        return response


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = AppUser.objects.all()
    permission_classes = [IsAdminReadOnly]
    required_fields = [
        "username",
        "password",
        "first_name",
        "confirm_password",
        "email",
        "last_name",
    ]

    def post(self, request, *args, **kwargs):

        data = dict(request.data)
        user_data = {item: data.get(item, [None])[0] for item in self.required_fields}

        for key, value in user_data.items():
            if not value:
                return Response(
                    {key: ["This field is reqired"]}, status=status.HTTP_400_BAD_REQUEST
                )

        password = user_data.get("password")
        confirm_password = user_data.get("confirm_password")
        has_error = validate_password(password, confirm_password)
        if has_error:
            info, stat = has_error
            return Response(info, stat)

        serialized_data = self.serializer_class(data=user_data)

        del user_data["confirm_password"]  # remove confirmation data
        user_data["is_active"] = False
        if serialized_data.is_valid():
            new_user = AppUser.objects.create_user(**user_data)
            act_token = ActivationToken.objects.create(user=new_user)
            return Response(
                dict(message="registration successfull", token=str(act_token.token)),
                status=status.HTTP_201_CREATED,
            )

        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


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
    search_fields = university_list_search_field

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

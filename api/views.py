from rest_framework.generics import (
        ListCreateAPIView,
        RetrieveUpdateDestroyAPIView)
from backend.models import University, Language
from cities_light.models import Country, City
from .serializers import UniversitySerializer
from rest_framework.response import Response
from rest_framework import status, filters, renderers
from django.contrib.auth.models import AnonymousUser
from .permissions import IsAdminOrReadOnly

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

        uni = University.objects.get(
                id=kwargs.get(self.lookup_field))

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
            city = City.objects.filter(
                    country=uni.country,
                    name=data["city"][0])
            if city:
                uni.city = city[0]
                uni.save()
        return Response(
                self.serializer_class(uni).data,
                status=response.status_code)


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
                dict(message="Only Permission denied"), status=status.HTTP_401_UNAUTHORIZED
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

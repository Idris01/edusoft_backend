from rest_framework.generics import ListCreateAPIView
from backend.models import University, Language
from cities_light.models import Country, City
from .serializers import UniversitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser


class UniversityListCreateAPIView(ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    # permission_classes = [IsAuthenticated]

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

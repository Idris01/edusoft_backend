from rest_framework.generics import ListCreateAPIView
from backend.models import University, Language
from cities_light.models import Country
from .serializers import UniversitySerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser


class UniversityListCreateAPIView(ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def post(self, request, *args, **kwargs):
        data = {key: ",".join(value) for key, value in dict(request.data).items()}
        if "country" in data:
            country_code = data.get("country")
            country = Country.objects.filter(code2__iexact=country_code)
            if country:
                data["country"] = country[0].id
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

            new_university = ""
            if not isinstance(request.user, AnonymousUser):
                new_university = UniversitySerializer(data=data, user=request.user)
            else:
                new_university = UniversitySerializer(data=data)

            if new_university.is_valid():
                new_university.save()
                return Response(new_university.data, status=status.HTTP_201_CREATED)
            return Response(new_university.errors, status=status.HTTP_400_BAD_REQUEST)

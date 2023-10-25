from rest_framework import serializers
from backend.models import University


class UniversitySerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = University
        fields = [
            "id",
            "name",
            "history",
            "languages",
            "created_by",
            "country",
            "city",
            "accomodation",
            "website",
        ]

    def get_languages(self, obj):
        languages = [item.name for item in obj.languages.all()]
        return languages

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_city(self, obj):
        return obj.city.name

    def get_country(self, obj):
        return obj.country.name

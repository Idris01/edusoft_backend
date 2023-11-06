from rest_framework import serializers
from backend.models import University, AppUser, Profile, Course
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import cities_light


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class UniversitySerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField(read_only=True)
    country_code = serializers.SerializerMethodField(read_only=True)

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
            "postal_code",
            "country_code",
        ]

    def get_languages(self, obj):
        languages = [item.name for item in obj.languages.all()]
        return languages

    def get_created_by(self, obj):
        if obj.created_by is not None:
            return obj.created_by.username

    def get_city(self, obj):
        if obj.city is not None:
            return obj.city.name

    def get_country(self, obj):
        if obj.country is not None:
            return obj.country.name

    def get_country_code(self, obj):
        if obj.country is not None:
            return obj.country.code2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["id", "username", "first_name", "last_name", "email", "is_active"]


class EdusoftObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.username
        token["email"] = user.email

        return token


class ProfileSerializer(serializers.ModelSerializer):
    nationality = serializers.SlugRelatedField(
        slug_field="code2", queryset=cities_light.models.Country.objects.all()
    )

    class Meta:
        model = Profile
        fields = "__all__"

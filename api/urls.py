from django.urls import path
from .views import (
        UniversityListCreateAPIView,
        UniversityDetailAPIView,
        UserListCreateAPIView,
        EdusoftTokenObtainPairView)
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "api"

urlpatterns = [
    path(
        "universities/",
        UniversityListCreateAPIView.as_view(),
        name="university_list_create"),
    path(
        "universities/<slug:id>",
        UniversityDetailAPIView.as_view(),
        name="university_detail"),
    path(
        "users/",
        UserListCreateAPIView.as_view(),
        name="user_list_create"),
    path(
        "token/",
        EdusoftTokenObtainPairView.as_view(),
        name="user_login")
]

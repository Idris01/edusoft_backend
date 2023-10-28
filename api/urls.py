from django.urls import path
from .views import (
        UniversityListCreateAPIView,
        UniversityDetailAPIView)

app_name = "api"

urlpatterns = [
    path(
        "universities/",
        UniversityListCreateAPIView.as_view(),
        name="university_list_create"),
    path(
        "universities/<slug:id>",
        UniversityDetailAPIView.as_view(),
        name="university_detail")
    
]

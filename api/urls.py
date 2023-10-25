from django.urls import path
from .views import UniversityListCreateAPIView

app_name = "api"

urlpatterns = [
    path(
        "universities/",
        UniversityListCreateAPIView.as_view(),
        name="university_list_create",
    )
]

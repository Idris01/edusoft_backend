from django.urls import path
from .views import (
    UniversityListCreateAPIView,
    UniversityDetailAPIView,
    UserListCreateAPIView,
    EdusoftTokenObtainPairView,
    VerifyAccountAPIView,
    PasswordResetAPIView,
    UserProfileAPIView,
    CourseListAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "api"

urlpatterns = [
    path(
        "universities/",
        UniversityListCreateAPIView.as_view(),
        name="university_list_create",
    ),
    path(
        "universities/<slug:id>",
        UniversityDetailAPIView.as_view(),
        name="university_detail",
    ),
    path("users/", UserListCreateAPIView.as_view(), name="user_list_create"),
    path("token/", EdusoftTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "account/<slug:token>/verify/",
        VerifyAccountAPIView.as_view(),
        name="verify_account",
    ),
    path(
        "accounts/password_reset/", PasswordResetAPIView.as_view(), name="password_reset"
    ),
    path("user/profile/", UserProfileAPIView.as_view(), name="profile_detail"),
    path("courses/list/", CourseListAPIView.as_view(), name="course_list"),
]

from django.urls import path

from .views import ProfileUpdateView, SignupView

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileUpdateView.as_view(), name="profile_update"),
    path("signup/", SignupView.as_view(), name="signup"),
]

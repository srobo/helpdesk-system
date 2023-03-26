from django.urls import path

from .views import OnboardingView, ProfileUpdateView, SignupView

app_name = "accounts"

urlpatterns = [
    path("onboarding/", OnboardingView.as_view(), name="onboarding"),
    path("profile/", ProfileUpdateView.as_view(), name="profile_update"),
    path("signup/", SignupView.as_view(), name="signup"),
]

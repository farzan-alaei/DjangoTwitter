from django.urls import path

from profiles.views import (
    UserProfileView,
    CustomLoginView,
    CustomLogoutView,
    ChangePasswordView,
    RegisterView,
    OtherProfileView,
)

app_name = "profiles"

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("profile/<int:id>/", OtherProfileView.as_view(), name="other_profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]

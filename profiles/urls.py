from django.urls import path

from profiles.views import (
    ProfileView,
    CustomLoginView,
    CustomLogoutView,
    ChangePasswordView,
    RegisterView,
)

app_name = "profiles"

urlpatterns = [
    path("edit-profile/", ProfileView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]

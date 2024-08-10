from django.urls import path

from profiles.views import ProfileView, CustomLoginView, CustomLogoutView, ChangePasswordView

app_name = "profiles"

urlpatterns = [
    path("form/", ProfileView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]

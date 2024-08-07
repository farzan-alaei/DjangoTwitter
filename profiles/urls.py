from django.urls import path
from profiles.views import ProfileView

urlpatterns = [
    path("form/", ProfileView.as_view(), name="profile"),
]
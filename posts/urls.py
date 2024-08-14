from django.urls import path
from posts.views import UserPostListView

urlpatterns = [
    path("my-posts/", UserPostListView.as_view(), name="posts"),
]
from django.urls import path
from posts.views import UserPostListView, FollowedUsersPostsListView

app_name = "posts"

urlpatterns = [
    path("my-posts/", UserPostListView.as_view(), name="user_posts"),
    path("followed-posts/", FollowedUsersPostsListView.as_view(), name="followed_posts"),
]
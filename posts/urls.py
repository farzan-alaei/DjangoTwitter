from django.urls import path
from posts.views import (
    UserPostListView,
    FollowedUsersPostsListView,
    CreatePostView,
    EditPostView,
    UserDetailPostView,
)

app_name = "posts"

urlpatterns = [
    path("my-posts/", UserPostListView.as_view(), name="user_posts"),
    path(
        "followed-posts/", FollowedUsersPostsListView.as_view(), name="followed_posts"
    ),
    path("create-post/", CreatePostView.as_view(), name="create_post"),
    path("edit-post/<int:pk>/", EditPostView.as_view(), name="edit_post"),
    path("detail-post/<int:pk>/", UserDetailPostView.as_view(), name="user_detail_post"),
]

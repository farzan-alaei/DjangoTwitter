from django.urls import path
from posts.views import (
    UserPostListView,
    CreatePostView,
    EditPostView,
    UserDetailPostView,
    OtherUserDetailPostView,
    TagPostsView,
    UnfollowTagView,
    FollowTagView,
)

app_name = "posts"

urlpatterns = [
    path("my-posts/", UserPostListView.as_view(), name="user_posts"),
    path("create-post/", CreatePostView.as_view(), name="create_post"),
    path("edit-post/<int:pk>/", EditPostView.as_view(), name="edit_post"),
    path(
        "detail-post/<int:pk>/", UserDetailPostView.as_view(), name="user_detail_post"
    ),
    path(
        "post/<int:pk>/",
        OtherUserDetailPostView.as_view(),
        name="other_user_detail_post",
    ),
    path('tag/<int:tag_id>/', TagPostsView.as_view(), name="tag_posts"),
    path("follow-tag/<int:tag_id>/", FollowTagView.as_view(), name="follow_tag"),
    path("unfollow-tag/<int:tag_id>/", UnfollowTagView.as_view(), name="unfollow_tag")
]

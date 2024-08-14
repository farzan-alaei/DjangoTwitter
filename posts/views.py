from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from posts.models import Post
from profiles.models import Follow


# Create your views here.


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"

    def get_queryset(self):
        return Post.objects.filter(archived=False, author=self.request.user)


class FollowedUsersPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "followed_user_posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"

    def get_queryset(self):
        followed_users = Follow.objects.filter(follower=self.request.user).values_list(
            "followed", flat=True
        )
        return Post.objects.filter(archived=False, author__in=followed_users)
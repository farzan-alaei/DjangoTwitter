from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from posts.forms import PostForm
from posts.models import Post
from profiles.models import Follow


# Create your views here.


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by(
            "-created_at"
        )


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


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "create_post.html"
    form_class = PostForm
    login_url = "profiles:login"
    success_url = reverse_lazy("posts:user_posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "پست شما با موفقیت ایجاد شد")
        return response


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "edit_post.html"
    form_class = PostForm
    login_url = "profiles:login"
    success_url = reverse_lazy("posts:user_posts")

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "پست شما با موفقیت ویرایش شد")
        return response


class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    login_url = "profiles:login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
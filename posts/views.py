from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.shortcuts import redirect
from posts.forms import PostForm
from posts.models import Post, Image, Like, Dislike
from profiles.models import Follow


# Create your views here.


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")


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
        images = self.request.FILES.getlist("image")
        for image in images:
            Image.objects.create(image=image, post=self.object)
        messages.success(self.request, "پست شما با موفقیت ایجاد شد")
        return response


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "edit_post.html"
    form_class = PostForm
    login_url = "profiles:login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist("image")
        for image in images:
            Image.objects.create(image=image, post=self.object)
        messages.success(self.request, "پست شما با موفقیت ویرایش شد")
        return response

    def get_success_url(self):
        return reverse("posts:user_detail_post", kwargs={"pk": self.object.pk})


class UserDetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "user_detail_post.html"
    context_object_name = "post"
    login_url = "profiles:login"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()

        context["user_liked"] = Like.objects.filter(user=user, post=post).exists()
        context["user_disliked"] = Dislike.objects.filter(user=user, post=post).exists()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        if "like" in request.POST:
            like_exists = Like.objects.filter(user=user, post=post).exists()
            dislike_exists = Dislike.objects.filter(user=user, post=post).exists()

            if dislike_exists:
                Dislike.objects.filter(user=user, post=post).delete()

            if not like_exists:
                Like.objects.create(user=user, post=post)
                messages.success(request, "You liked this post.")
            else:
                Like.objects.filter(user=user, post=post).delete()
                messages.success(request, "You unliked this post.")

        elif "dislike" in request.POST:
            dislike_exists = Dislike.objects.filter(user=user, post=post).exists()
            like_exists = Like.objects.filter(user=user, post=post).exists()

            if like_exists:
                Like.objects.filter(user=user, post=post).delete()

            if not dislike_exists:
                Dislike.objects.create(user=user, post=post)
                messages.success(request, "You disliked this post.")
            else:
                Dislike.objects.filter(user=user, post=post).delete()
                messages.success(request, "You undisliked this post.")

        return redirect("posts:user_detail_post", pk=post.pk)

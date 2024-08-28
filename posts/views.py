from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.shortcuts import get_object_or_404
from django.db.models import Q

from posts.forms import PostForm, SearchForm, CommentForm
from posts.models import Post, Image, Like, Dislike, Tag, Comment, TagFollow
from profiles.models import Follow
from profiles.models import Profile


# Create your views here.


class SearchView(ListView):
    """
    View for search
    """

    template_name = "search_results.html"
    context_object_name = "search_results"

    def get_queryset(self):
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET or None)
        query = ""
        profiles = []
        posts = []
        tags = []

        if form.is_valid():
            query = form.cleaned_data.get("query", "")
            if query:
                profiles = Profile.objects.filter(
                    user__username__icontains=query, archived=False
                )
                posts = Post.objects.filter(title__icontains=query, archived=False)
                tags = Tag.objects.filter(name__icontains=query)

        context.update(
            {
                "form": form,
                "query": query,
                "profiles": profiles,
                "posts": posts,
                "tags": tags,
            }
        )
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    """
    View for user posts
    """

    model = Post
    template_name = "user_posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    View for creating post
    """

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
        messages.success(self.request, "your post has been created")
        return response


class EditPostView(LoginRequiredMixin, UpdateView):
    """
    View for editing post
    """

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
        messages.success(self.request, "your post has been updated")
        return response

    def get_success_url(self):
        return reverse("posts:user_detail_post", kwargs={"pk": self.object.pk})


class UserDetailPostView(LoginRequiredMixin, DetailView):
    """
    View for user's post
    """

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

        comments = Comment.objects.filter(post=post, parent=None).order_by(
            "-created_at"
        )
        context["comments"] = comments
        context["comment_form"] = CommentForm()

        context["user_liked"] = Like.objects.filter(user=user, post=post).exists()
        context["user_disliked"] = Dislike.objects.filter(user=user, post=post).exists()
        return context

    def post(self, request, *args, **kwargs):
        """
        Add like or dislike and comment to post
        """
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
        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = user
                comment.post = post
                parent_id = request.POST.get("parent_id")
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                comment.save()
                messages.success(request, "Your comment was added successfully.")
            else:
                messages.error(request, "There was an error adding your comment.")
        return redirect("posts:user_detail_post", pk=post.pk)


class OtherUserDetailPostView(DetailView):
    """
    View for other user's post
    """

    model = Post
    template_name = "other_detail_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get("pk")
        post = get_object_or_404(Post, pk=post_id)

        comments = Comment.objects.filter(post=post, parent=None).order_by(
            "-created_at"
        )
        context["comments"] = comments
        context["comment_form"] = CommentForm()

        if self.request.user.is_authenticated:
            user = self.request.user
            context["user_liked"] = Like.objects.filter(user=user, post=post).exists()
            context["user_disliked"] = Dislike.objects.filter(
                user=user, post=post
            ).exists()
        context["post"] = post
        return context

    def post(self, request, *args, **kwargs):
        """
        Add like or dislike and comment to post
        """
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

        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = user
                comment.post = post
                parent_id = request.POST.get("parent_id")
                if parent_id:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                comment.save()
                messages.success(request, "Your comment was added successfully.")
            else:
                messages.error(request, "There was an error adding your comment.")

        return redirect("posts:other_user_detail_post", pk=post.pk)


class FollowTagView(LoginRequiredMixin, View):
    """
    View for following a tag.
    """

    def post(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)

        if not TagFollow.objects.filter(user=request.user, tag=tag).exists():
            TagFollow.objects.create(user=request.user, tag=tag)

        return HttpResponseRedirect(
            reverse_lazy("posts:tag_posts", kwargs={"tag_id": tag_id})
        )


class UnfollowTagView(LoginRequiredMixin, View):
    """
    View for unfollowing a tag.
    """

    def post(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        follow = TagFollow.objects.filter(user=request.user, tag=tag).first()
        if follow:
            follow.delete()

        return HttpResponseRedirect(
            reverse_lazy("posts:tag_posts", kwargs={"tag_id": tag_id})
        )


class TagPostsView(ListView):
    """
    View for displaying posts for a specific tag.
    """

    model = Post
    template_name = "tag_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_id = self.kwargs.get("tag_id")
        return Post.objects.filter(tags__id=tag_id, archived=False).order_by(
            "-created_at"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get("tag_id")
        context["tag"] = get_object_or_404(Tag, id=tag_id)
        if self.request.user.is_authenticated:
            context["is_following_tag"] = TagFollow.objects.filter(
                user=self.request.user, tag__id=tag_id
            ).exists()
        return context


class TimeLineView(ListView):
    """
    View for displaying the timeline.
    """

    model = Post
    template_name = "timeline.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            followed_users = Follow.objects.filter(
                follower=self.request.user
            ).values_list("followed", flat=True)
            followed_tags = TagFollow.objects.filter(
                user=self.request.user
            ).values_list("tag", flat=True)
            return (
                Post.objects.filter(archived=False)
                .filter(
                    Q(author__in=followed_users)
                    | Q(tags__in=followed_tags)
                    | Q(author=self.request.user)
                )
                .distinct()
                .order_by("-created_at")
            )
        else:
            return Post.objects.filter(archived=False).order_by("-created_at")[:10]


class TagFollowListView(ListView):
    """
    View for displaying the list of tags followed by the current user.
    """

    model = Tag
    template_name = "tag_list.html"
    context_object_name = "tags"
    paginate_by = 10

    def get_queryset(self):
        return Tag.objects.filter(followers__user=self.request.user)

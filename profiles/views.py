from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View
from django.views.generic.edit import UpdateView, CreateView
from django.core.paginator import Paginator

from profiles.forms import ProfileForm, RegisterForm, LoginForm, ChangePasswordForm
from profiles.models import Profile, Follow
from posts.models import Post
from django.contrib.auth.models import User


# Create your views here.
class OtherProfileView(TemplateView):
    template_name = "other_profile.html"
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs.get("id")
        profile = get_object_or_404(Profile, pk=profile_id)
        posts = Post.objects.filter(author=profile.user, archived=False).order_by(
            "-created_at", "-updated_at"
        )

        # Implement pagination
        paginator = Paginator(posts, 12)  # Show 4 posts per page
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["profile"] = profile
        context["posts"] = page_obj
        if self.request.user.is_authenticated:
            context["is_following"] = Follow.objects.filter(
                follower=self.request.user, followed=profile.user
            ).exists()
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("profiles:user_profile")
    login_url = "profiles:login"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.is_valid():
            form.save()
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get("next", "/")


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = "profiles:user_profile"
    login_url = "profiles:login"


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    login_url = "profiles:login"
    form_class = ChangePasswordForm
    success_url = reverse_lazy("profiles:change_password")

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully")
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = "index.html"


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        username = self.request.POST["username"]
        password = self.request.POST["password1"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Registration successful")
        # Create Profile for user after registration
        Profile.objects.create(user=user)
        return HttpResponseRedirect(self.success_url)


class FollowView(LoginRequiredMixin, View):
    """
    View for following a user.
    """

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)
        profile_to_follow = get_object_or_404(Profile, user=user_to_follow)

        if request.user == user_to_follow:
            return redirect(
                reverse_lazy(
                    "profiles:other_profile", kwargs={"id": profile_to_follow.id}
                )
            )

        # Check if the follow relationship already exists
        if not Follow.objects.filter(
            follower=request.user, followed=user_to_follow
        ).exists():
            Follow.objects.create(follower=request.user, followed=user_to_follow)

        return redirect(
            reverse_lazy("profiles:other_profile", kwargs={"id": profile_to_follow.id})
        )


class UnfollowView(LoginRequiredMixin, View):
    """
    View for unfollowing a user.
    """

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        profile_to_unfollow = get_object_or_404(Profile, user=user_to_unfollow)

        if request.user == user_to_unfollow:
            return redirect(
                reverse_lazy(
                    "profiles:other_profile", kwargs={"id": profile_to_unfollow.id}
                )
            )

        # Find and delete the follow relationship
        follow = Follow.objects.filter(
            follower=request.user, followed=user_to_unfollow
        ).first()
        if follow:
            follow.delete()

        return redirect(
            reverse_lazy(
                "profiles:other_profile", kwargs={"id": profile_to_unfollow.id}
            )
        )

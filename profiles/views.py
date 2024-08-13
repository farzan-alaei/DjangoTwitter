from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.http import HttpResponseRedirect

from profiles.forms import ProfileForm, RegisterForm, LoginForm


# Create your views here.


class ProfileView(FormView):
    template_name = "profile.html"
    form_class = ProfileForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    form_class = LoginForm

    def get_success_url(self):
        return self.request.GET.get("next", "/")


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = "profiles:profile"
    login_url = "profiles:login"


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "change_password.html"
    login_url = "profiles:login"

    def get_success_url(self):
        return self.request.GET.get("next", "/")


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
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

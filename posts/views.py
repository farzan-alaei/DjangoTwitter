from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from posts.models import Post


# Create your views here.


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    login_url = "profiles:login"

    def get_queryset(self):
        return Post.objects.filter(archived=False, author=self.request.user)

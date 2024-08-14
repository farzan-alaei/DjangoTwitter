from django.shortcuts import render
from django.views.generic import ListView
from posts.models import Post, Image, Like, Dislike, Comment
# Create your views here.


class PostListView(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.all()
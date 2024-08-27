from django.contrib import admin
from posts.models import Post, Image, Like, Dislike, Comment, Tag, TagFollow

# Register your models here.


class ImageInline(admin.TabularInline):
    model = Image


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    inlines = [
        ImageInline,
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(TagFollow)

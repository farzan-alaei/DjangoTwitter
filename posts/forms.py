from django import forms
from django_select2.forms import ModelSelect2TagWidget

from posts.models import Post, Image, Tag


class TagWidget(ModelSelect2TagWidget):
    search_fields = ["name__icontains"]

    def value_from_datadict(self, data, files, name):
        values = super().value_from_datadict(data, files, name)
        tags = []
        for value in values:
            if value.isdigit():
                tags.append(value)
            else:
                tag, created = Tag.objects.get_or_create(name=value)
                tags.append(tag.id)
        return tags


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ["image"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "featured_image", "content", "tags", "archived"]
        widgets = {
            "tags": TagWidget(
                model=Tag,
                search_fields=["name__icontains"],
            )
        }

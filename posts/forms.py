from django import forms
from django_select2.forms import ModelSelect2TagWidget

from posts.models import Post, Image, Tag, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 2, "placeholder": "Write a comment..."}
            ),
        }


class TagWidget(ModelSelect2TagWidget):
    search_fields = ["name__icontains"]

    def value_from_datadict(self, data, files, name):
        """
        Overrides the default method `value_from_datadict` to retrieve tag values
        from the form data.

        Retrieves the values from the form data, and converts them into a list of
        primary keys. If the value is a digit, it is assumed to be a primary key
        of an existing tag. If the value is not a digit, it is assumed to be a
        tag name. It then searches for an existing tag with the given name, and
        if none is found, it creates a new one. The primary key of the tag is
        appended to the list of primary keys.

        Returns:
            list: A list of primary keys of tags.
        """
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


class LikeForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput())


class DislikeForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput())


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
            }
        ),
    )

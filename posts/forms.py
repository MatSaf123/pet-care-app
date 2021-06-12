from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'country',
            'city',
            'street_address',
            'tags',
            'type_of_post',
        ]

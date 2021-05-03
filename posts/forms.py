from django import forms
from django.shortcuts import get_object_or_404, render

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tags',
        ]

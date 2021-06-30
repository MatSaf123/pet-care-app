from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile, Comment


class UserRegisterForm(UserCreationForm):
    """Form for registering a new user."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form for updating user info (associated with the User model)."""

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user info on his profile (associated with the Profile model)."""

    class Meta:
        model = Profile
        fields = ['profile_pic', 'phone_number', 'country', 'city', 'description']


class CommentForm(forms.ModelForm):
    """Form for creating new comments on user's profiles."""

    class Meta:
        model = Comment
        fields = ['content']

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView

from posts.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CommentForm

# Create your views here.
from .models import Comment


def register(request):
    """Register new user

    :param request: user request
    """

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_edit(request):
    """Edit (currently logged-in) user profile

    :param request: user request
    """

    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile-edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile_edit.html', context)


def user_profile_view(request, username):
    """Return render of a user profile page

    :param request: user request
    :param username: username of requested profile owner
    """

    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    comments = Comment.objects.filter(profile=user.profile)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.profile = user.profile
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'profile_owner': user,
        'posts': posts,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'users/profile_detail.html', context)
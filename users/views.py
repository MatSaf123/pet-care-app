from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DeleteView

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
            comment = comment_form.save(commit=False)
            comment.profile = user.profile
            comment.author = request.user
            comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'profile_owner': user,
        'posts': posts,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'users/profile_detail.html', context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Comment delete view"""

    model = Comment

    def get_success_url(self):
        """Redirect to user profile page after deleting comment"""

        username = self.kwargs['username']
        return reverse('user-profile', kwargs={'username': username})

    def test_func(self):
        """Check if user trying to delete the comment is it's author"""

        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

def all_users_view(request):
    """Get all users list. Alternatively, get filtered users list"""

    if request.method == 'POST':
        # filter by requested username
        username = request.POST.get("reqested_username")
        users = User.objects.filter(username__startswith=username)
    else:
        users = User.objects.all()

    return render(request, 'users/all_users.html', {'users': users})

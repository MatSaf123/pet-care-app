from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView

from .models import Post


# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, '../templates/posts/home.html', context)


def about(request):
    return render(request, '../templates/posts/about.html', {'title': 'About'})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

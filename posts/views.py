from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from django.views.generic import CreateView

from .models import Post
from taggit.models import Tag


# Create your views here.


def home_view(request):
    posts = Post.objects.all()

    # Show most common tags (top four)
    common_tags = Post.tags.most_common()[:4]

    context = {
        'posts': posts,
        'common_tags': common_tags,
    }
    return render(request, '../templates/posts/home.html', context)


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    return render(request, '../templates/posts/detail.html', context)


def tagged(request, slug):
    """Filter posts by tag name"""

    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, '../templates/posts/home.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags']

    def form_valid(self, form):

        form.instance.author = self.request.user
        new_post = form.save(commit=False)
        new_post.slug = slugify(new_post.title)
        new_post.save()
        form.save_m2m()

        return super().form_valid(form)


def about(request):
    return render(request, '../templates/posts/about.html', {'title': 'About'})

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from django.views.generic import CreateView, DeleteView

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

    try:
        post_id = str(1 + Post.objects.latest('id').id)
    except model.DoesNotExist:
        post_id = '0'

    def form_valid(self, form):
        form.instance.author = self.request.user
        new_post = form.save(commit=False)

        # in order to create unique slug, id number is added at the end of it
        new_post.slug = slugify(''.join([new_post.title, self.post_id]))

        new_post.save()
        form.save_m2m()

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # check if active user is the original poster
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, '../templates/posts/about.html', {'title': 'About'})

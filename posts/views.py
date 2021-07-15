from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import Post
from taggit.models import Tag
from .geolocation import get_client_ip, get_geo_from_ip, get_geo_data_from_api, initiate_map
import folium
import string
import random
from django.contrib import messages

# Create your views here.


def home_view(request) -> HttpResponse:
    """View for displaying the home page, containing posts list and an interactive map render.

    :param request: user request
    """

    if request.method == 'POST':
        type_of_post = request.POST.get("type_of_post")
        if not type_of_post:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(type_of_post=type_of_post)
    else:
        posts = Post.objects.all()

    # Show most common tags (top four)
    common_tags = Post.tags.most_common()[:4]

    # Initiate the map
    ip = get_client_ip(request)
    m, skipped_posts_count = initiate_map(posts, get_geo_from_ip(ip))
    
    if skipped_posts_count > 0:
        messages.warning(request, f'Couldn\'t load {skipped_posts_count} post marker(s) on the map.')
    
    context = {
        'posts': posts,
        'common_tags': common_tags,
        'map': m
    }

    return render(request, '../templates/posts/home.html', context)


def detail_view(request, slug) -> HttpResponse:
    """View for displaying detail screen of a post, with it's detail info
    and an interactive map render.

    :param request: user request
    :param slug: slug value of a post, needed to get post from the database
    """

    post = get_object_or_404(Post, slug=slug)

    m, skipped_posts_count = initiate_map([post], None)

    if skipped_posts_count > 0:
        messages.warning(request, f'Couldn\'t load post marker on the map.')

    context = {
        'post': post,
        'map': m
    }

    return render(request, '../templates/posts/detail.html', context)


def tagged_view(request, slug) -> HttpResponse:
    """View for displaying home page containing only posts tagged with chosen tag.

    :param request: user request
    :param slug: slug value of a post, needed to get post from the database
    """

    if request.method == 'POST':
        type_of_post = request.POST.get("type_of_post")
        if not type_of_post:
            posts = Post.objects.all()
        else:
            posts = Post.objects.filter(type_of_post=type_of_post)
    else:
        posts = Post.objects.all()

    tag = get_object_or_404(Tag, slug=slug)
    posts = posts.filter(tags=tag)

    # Initiate the map
    ip = get_client_ip(request)
    m, skipped_posts_count = initiate_map(posts, get_geo_from_ip(ip))

    if skipped_posts_count > 0:
        messages.warning(request, f'Couldn\'t load {skipped_posts_count} post marker(s) on the map.')

    context = {
        'tag': tag,
        'posts': posts,
        'map': m
    }

    return render(request, '../templates/posts/home.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new post."""

    model = Post
    fields = ['title', 'content', 'country', 'city',
              'street_address', 'tags', 'type_of_post']

    def form_valid(self, form) -> HttpResponse:
        """If form is valid, create a slug value for it and save the post."""

        form.instance.author = self.request.user
        new_post = form.save(commit=False)
        # random string to add to the slug
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for i in range(16))
        new_post.slug = slugify(''.join([new_post.title, random_string]))
        new_post.save()
        form.save_m2m()

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a post."""

    model = Post
    success_url = '/'

    # check if active user is the original poster
    def test_func(self) -> bool:
        """Check if user trying to delete the post is it's author."""

        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating (editing) a post."""

    model = Post
    fields = ['title', 'content', 'country', 'city',
              'street_address', 'tags', 'type_of_post']

    def get_context_data(self, **kwargs) -> dict:
        """Get context with post data to fill form when editing."""

        slug = self.kwargs['slug']
        post = Post.objects.get(slug=slug)

        title = post.title
        content = post.content
        country = post.country
        city = post.city
        street_address = post.street_address
        tags = ','.join([str(tag) for tag in post.tags.all()])
        type_of_post = post.type_of_post

        context = {
            'title': title,
            'content': content,
            'country': country,
            'city': city,
            'street_address': street_address,
            'tags': tags,
            'type_of_post': type_of_post
        }

        return context

    def form_valid(self, form) -> HttpResponse:
        """If form is valid, update post."""

        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self) -> bool:
        """Check if user trying to edit the post is it's author"""

        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about_view(request) -> HttpResponse:
    """View for displaying 'About' page.

    :param request: user request
    """

    return render(request, '../templates/posts/about.html', {'title': 'About'})


def all_tags_view(request) -> HttpResponse:
    """View for displaying page with all tags listed on it.

    :param request: user request
    """

    if request.method == 'POST':
        # filter by requested username
        requested_tag = request.POST.get("requested_tag")
        tags = Post.tags.filter(name__startswith=requested_tag).order_by('name')
    else:
        tags = Post.tags.all().order_by('name')

    return render(request, '../templates/posts/all_tags.html', {'tags': tags})

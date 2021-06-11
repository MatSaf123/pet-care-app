from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import Post
from taggit.models import Tag

# Utils
import string
import random

# Geolocation
from .geolocation import get_client_ip, get_geo_from_ip, get_geo_data_from_api, initiate_map
import folium

# Create your views here.


def home_view(request):
    """Return render of home page with posts list and an interactive map

    :param request: user request
    """

    # TODO: add POST method for filtering help requests and help offers
    posts = Post.objects.all()
    # Show most common tags (top four)
    common_tags = Post.tags.most_common()[:4]
    ip = get_client_ip(request)
    m = initiate_map(posts, get_geo_from_ip(ip))

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'map': m
    }
    return render(request, '../templates/posts/home.html', context)


def detail_view(request, slug):
    """Return render of a post detail page, with it's content and an interactive map

    :param request: user request
    :param slug: slug value of a post, needed to get post from the database
    """

    post = get_object_or_404(Post, slug=slug)
    location = get_geo_data_from_api(' '.join([post.street_address, post.city, post.country]))

    if post.type_of_post == 'HO':
        color = 'blue'
    else:
        color = 'red'

    m = folium.Map(width=500, height=310, location=(location.latitude, location.longitude), zoom_start=16)
    folium.Marker([location.latitude, location.longitude], icon=folium.Icon(color=color)).add_to(m)
    m = m._repr_html_()

    context = {
        'post': post,
        'map': m
    }
    return render(request, '../templates/posts/detail.html', context)


def tagged(request, slug):
    """Filter posts by picked tag name

    :param request: user request
    :param slug: slug value of a post, needed to get post from the database
    """

    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    ip = get_client_ip(request)
    m = initiate_map(posts, get_geo_from_ip(ip))

    context = {
        'tag': tag,
        'posts': posts,
        'map': m
    }
    return render(request, '../templates/posts/home.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Post creation view"""

    model = Post
    fields = ['title', 'content', 'country', 'city', 'street_address', 'tags', 'type_of_post']

    def form_valid(self, form):
        """If form is valid, create a slug value for it and save the post"""

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
    """Post delete view"""

    model = Post
    success_url = '/'

    # check if active user is the original poster
    def test_func(self):
        """Check if user trying to delete the post is it's author"""

        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Post update view"""

    model = Post
    fields = ['title', 'content', 'country', 'city', 'street_address', 'tags', 'type_of_post']

    def get_context_data(self, **kwargs):
        """Get context with post data to fill form when editing"""

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

    def form_valid(self, form):
        """If form is valid, update post"""

        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Check if user trying to edit the post is it's author"""

        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    """Return render of a about page

    :param request: user request
    """

    return render(request, '../templates/posts/about.html', {'title': 'About'})


def all_tags_view(request):
    """List all available tags

    :param request: user request
    """

    if request.method == 'POST':
        # filter by requested username
        requested_tag = request.POST.get("requested_tag")
        tags = Post.tags.filter(name__startswith=requested_tag)
    else:
        tags = Post.tags.all()

    
    return render(request, '../templates/posts/all_tags.html', {'tags': tags})

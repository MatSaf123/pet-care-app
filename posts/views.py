from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.views.generic import CreateView, DeleteView, UpdateView
from .models import Post
from taggit.models import Tag

# Utils
import string
import random

# Geolocation
from .geolocation import get_client_ip, get_geo, get_geo_data_from_api, initiate_map
import folium

# Create your views here.


def home_view(request):
    posts = Post.objects.all()

    # Show most common tags (top four)
    common_tags = Post.tags.most_common()[:4]

    ip = get_client_ip(request)
    m = initiate_map(posts, get_geo(ip))

    context = {
        'posts': posts,
        'common_tags': common_tags,
        'map': m
    }
    return render(request, '../templates/posts/home.html', context)


def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    location = get_geo_data_from_api(' '.join([post.street_address, post.city, post.country]))

    m = folium.Map(width=500, height=310, location=(location.latitude, location.longitude), zoom_start=16)
    folium.Marker([location.latitude, location.longitude], icon=folium.Icon(color='red')).add_to(m)

    m = m._repr_html_()

    context = {
        'post': post,
        'map': m
    }
    return render(request, '../templates/posts/detail.html', context)


def tagged(request, slug):
    """Filter posts by tag name"""

    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)

    ip = get_client_ip(request)
    m = initiate_map(posts, get_geo(ip))

    context = {
        'tag': tag,
        'posts': posts,
        'map': m
    }
    return render(request, '../templates/posts/home.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'country', 'city', 'street_address', 'tags']

    def form_valid(self, form):
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
    model = Post
    success_url = '/'

    # check if active user is the original poster
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'country', 'city', 'street_address', 'tags']

    def get_context_data(self, **kwargs):
        """Get context with post data to fill form when editing
        """

        # context = super(PostUpdateView, self).get_context_data(**kwargs)

        slug = self.kwargs['slug']

        post_data = Post.objects.filter(slug=slug)

        title = post_data[0].title
        content = post_data[0].content
        country = post_data[0].country
        city = post_data[0].city
        street_address = post_data[0].street_address

        tags = [str(tag) for tag in post_data[0].tags.all()]
        tags = ','.join(tags)

        return {'title': title, 'content': content, 'country': country, 'city': city, 'street_address': street_address,
                'tags': tags}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, '../templates/posts/about.html', {'title': 'About'})

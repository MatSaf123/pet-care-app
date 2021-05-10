from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.


class Post(models.Model):
    """Post model: a help request or help offer posted by a registered user"""

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100, default=None)
    tags = TaggableManager()

    country = models.CharField(max_length=100, default=None)
    city = models.CharField(max_length=100, default=None)
    street_address = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Redirect user to home page after a post is created"""
        return reverse('home')

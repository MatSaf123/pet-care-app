from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.


class Post(models.Model):
    """Post model: a help request or help offer posted by a registered user"""

    HELP_REQUEST = 'HR'
    HELP_OFFER = 'HO'

    TYPES_OF_POSTS = [
        (HELP_REQUEST, 'HELP_REQUEST'),
        (HELP_OFFER, 'HELP_OFFER'),
    ]    

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100, default=None)
    tags = TaggableManager()
    
    # ADDRESS
    country = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    street_address = models.CharField(max_length=100, default='')

    type_of_post = models.CharField( max_length=2, choices=TYPES_OF_POSTS, default=HELP_REQUEST)


    def __str__(self):
        """Return string representation of a Post"""

        return self.title

    def get_absolute_url(self):
        """Redirect user to home page after a post is created"""

        return reverse('home')

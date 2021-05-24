from django.db import models
from django.contrib.auth.models import User

# Pillow
from PIL import Image


# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """Profile model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.png', upload_to='profile_pictures')
    phone_number = PhoneNumberField(default='', null=True, blank=True)
    country = models.CharField(default='', max_length=64, null=True, blank=True)
    city = models.CharField(default='', max_length=64, null=True, blank=True)
    description = models.TextField(default='', max_length=255, null=True, blank=True)

    def __str__(self):
        """Return string representation of a profile"""

        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Save profile in the database"""

        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        # Scaling down too big pictures to 300x300 px
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

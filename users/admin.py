from django.contrib import admin
from users.models import Profile
from users.models import Comment


# Register your models here.

admin.site.register(Profile)
admin.site.register(Comment)

from django.urls import path
from . import views
from .views import PostCreateView

urlpatterns = [
    path('', views.home, name='posts-home'),
    path('about/', views.about, name='posts-about'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
]

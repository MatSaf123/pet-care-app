from django.urls import path
from . import views
from .views import detail_view, tagged_view, PostCreateView, PostDeleteView, PostUpdateView, all_tags_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/', detail_view, name="post-detail"),
    path('tag/<slug:slug>/', tagged_view, name="tagged"),
    path('tags/', views.all_tags_view, name="all-tags"),
]
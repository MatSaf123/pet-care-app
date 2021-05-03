from django.urls import path
from . import views
from .views import detail_view, tagged, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about, name='about'),

    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),

    path('post/<slug:slug>/', detail_view, name="post-detail"),
    path('tag/<slug:slug>/', tagged, name="tagged"),
]

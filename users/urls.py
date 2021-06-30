from django.urls import path, include
from . import views

urlpatterns = [
    path('edit/', views.profile_edit, name='profile-edit'),
    path('user/<str:username>', views.user_profile_view, name='user-profile'),
    path('user/<str:username>/<int:pk>', views.CommentDeleteView.as_view(), name='user-profile-delete-comment'),
    path('users/', views.all_users_view, name='users')
]
from django.http import request
from posts.views import PostCreateView
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Post
from django.utils import timezone
import random

class TestViews(TestCase):

    def setUp(self):
        """Run before tests."""

        self.user_1 = User.objects.create(
            username='test_user_1',
            email='test_user@example.com',
            password='testing123'
        )
        self.post_1 = Post.objects.create(
            title='test post 1',
            content='test_content',
            date_posted=timezone.now(),
            author=self.user_1,
            country='Poland',
            city='Katowice',
            type_of_post='HR',
        )
        self.post_2 = Post.objects.create(
            title='test post 2',
            content='test_content',
            date_posted=timezone.now(),
            author=self.user_1,
            country='Poland',
            city='Katowice',
            type_of_post='HO',
        )

        self.post_1.tags.set('test_1')
        self.post_2.tags.set('test_2')

        self.client = Client()
        self.home_url = reverse('home')
        self.detail_url = reverse('post-detail', args=[self.post_1.slug])
        self.tagged_url = reverse('tagged', args=['test_1'])
        self.create_url = reverse('post-create')
        self.update_url = reverse('post-update', args=[self.post_1.slug])


    def test_home_view_GET(self):

        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
    
    def test_home_view_POST(self):
        """POST sorting form and get sorted posts list returned."""

        response = self.client.post(self.home_url, {'type_of_post': 'HR'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')

        # check if returned list contains only help requests (HR)
        self.assertTrue(response.context['posts'][0] == self.post_1)
    
    def test_home_view_POST_no_data(self):

        response = self.client.post(self.home_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')

        # check if returned list contains all posts
        self.assertTrue(response.context['posts'].count() == 2)

    def test_detail_view_GET(self):

        response = self.client.post(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/detail.html')

    def test_tagged_GET(self):

        response = self.client.get(self.tagged_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
        self.assertTrue(response.context['posts'].count() == 1)
    
    def test_tagged_POST(self):

        response = self.client.post(self.tagged_url, {'type_of_post': 'HO'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/home.html')
        self.assertTrue(response.context['posts'].count() == 0)

    def test_post_create_GET_not_logged_in(self):
        
        response = self.client.get(self.create_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_post_create_GET_logged_in(self):
        
        self.client.force_login(self.user_1, backend=None)
        response = self.client.get(self.create_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')

    def test_edit_post_user_authorized(self):
        
        self.client.force_login(self.user_1, backend=None)
        response = self.client.post(self.update_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_form.html')

    def test_edit_post_user_not_authorized(self):

        response = self.client.post(self.update_url)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={self.update_url}')
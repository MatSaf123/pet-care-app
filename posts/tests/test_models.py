from django.test import TestCase
from posts.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

class TestModels(TestCase):

    def setUp(self):

        self.user_1 = User.objects.create(
            username='test_user_1',
            email='test_user@example.com',
            password='testing123'
        )
        self.post_1 = Post.objects.create(
            title='test post one',
            content='test_content',
            date_posted=timezone.now(),
            author=self.user_1,
            country='Poland',
            city='Katowice',
            type_of_post='HR',
        )

        self.post_1.save()
    
    def test_project_is_assigned_slug_on_creation(self):
        self.assertEquals(self.post_1.slug, 'test-post-one-1')
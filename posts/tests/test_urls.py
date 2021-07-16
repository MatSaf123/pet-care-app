from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts.views import home_view, detail_view, all_tags_view, PostCreateView, PostUpdateView, PostDeleteView


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home_view)

    def test_detail_url_is_resolved(self):
        url = reverse('post-detail', args=['some-slug'])
        self.assertEquals(resolve(url).func, detail_view)

    def test_all_tags_url_is_resolved(self):
        url = reverse('all-tags')
        self.assertEquals(resolve(url).func, all_tags_view)

    def test_add_post_url_is_resolved(self):
        url = reverse('post-create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_update_post_url_is_resolved(self):
        url = reverse('post-update', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_delete_post_url_is_resolved(self):
        url = reverse('post-delete', args=['some-slug'])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)
from django.test.testcases import SimpleTestCase
from posts.forms import PostForm


class TestForms(SimpleTestCase):

    def test_post_form_valid_data(self):
        form = PostForm(
            data = {
                'title' : 'test post',
                'content' : 'test content',
                'country' : 'Poland',
                'city' : 'Katowice',
                'street_address' : '', # not required
                'tags' : 'test,post,one',
                'type_of_post' : 'HR',
            }
        )

        self.assertTrue(form.is_valid())

    def test_post_form_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6) # one for every empty field
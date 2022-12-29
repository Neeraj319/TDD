from django.contrib.auth.models import User
from django.test import TestCase
from core.models import Blog

# Create your tests here.


class BlogTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="ram", password="ram123")

        self.blog = Blog.objects.create(
            title="test blog",
            body=""" this is a nice body haina fjlkadsfjasldkfjasdlkfjsd this is a nice blog etc etc """,
            user=self.user,
        )

    def test_blog_string(self):
        self.assertEqual(str(self.blog), "ram | test blog")

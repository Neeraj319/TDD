from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import Blog
from core.serializers import BlogSerializerResponse

# Create your tests here.


class BlogViewsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="someone", password="some password"
        )
        self.blogs = [
            Blog.objects.create(
                title="something",
                body="some random blog title dosenot matter",
                user=self.user,
            ),
            Blog.objects.create(
                title="extra123",
                body="some random blog body dosenot matter",
                user=self.user,
            ),
            Blog.objects.create(
                title="some crap",
                body="this is a test case1234432",
                user=self.user,
            ),
        ]

    def test_all_blogs(self):
        response = self.client.get(reverse("blogs-list"))
        blogs = BlogSerializerResponse(self.blogs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(blogs.data, response.json())

    def test_blog_by_id(self):
        response = self.client.get("/blogs/1", follow=True)
        blog = BlogSerializerResponse(self.blogs[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(blog.data, response.json())

    def test_blog_create(self):
        token = self.client.post(
            reverse("obtain_token"),
            data=dict(username="someone", password="some password"),
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(
            "/blogs/",
            data={
                "title": "some",
                "body": "Lorem Ipsum is simply dummy text of the printing and typesetting",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_blog_with_bad_body(self):
        token = self.client.post(
            reverse("obtain_token"),
            data=dict(username="someone", password="some password"),
        ).json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post(
            "/blogs/",
            data={
                "title": "some fsjflkasdjfasldkjfaslkd",
                "body": "Lorem Ipsum is simply dummy text of the printing and typesetting",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_blog_create_without_credentials(self):
        response = self.client.post(
            "/blogs/",
            data={
                "title": "some",
                "body": "Lorem Ipsum is simply dummy text of the printing and typesetting",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

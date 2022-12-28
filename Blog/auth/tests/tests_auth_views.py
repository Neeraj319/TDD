from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from auth.serializers import UserRegisterSerializer
from rest_framework.test import APIRequestFactory


class AuthViewTest(TestCase):
    def setUp(self) -> None:
        self.user_json = {"username": "kxa", "password": "12jsjfalkdfjaldfja"}
        User.objects.create_user(**self.user_json)

    def test_register(self):
        mock_data = {"username": "herokto", "password": "helloKcadfa@@@@"}
        response = self.client.post(reverse("register"), data=mock_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_bad_credentials(self):
        data = {"username": "", "password": ""}
        response = self.client.post(path=reverse("register"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_bad_password(self):
        data = {"username": "hello", "password": "herokta"}
        response = self.client.post(path=reverse("register"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_same_username(self):
        response = self.client.post(path=reverse("register"), data=self.user_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

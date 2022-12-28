from django.urls import path
from auth.views import RegisterUserAPIView, CustomAuthToken


urlpatterns = [
    path("login/", CustomAuthToken.as_view(), name="obtain_token"),
    path("register/", RegisterUserAPIView.as_view(), name="register"),
]

from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from auth.serializers import UserRegisterSerializer, UserResposeSerializer
from rest_framework import views
from rest_framework import status


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class RegisterUserAPIView(views.APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                data=UserResposeSerializer(user).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

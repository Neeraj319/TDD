from django.contrib.auth.models import User
from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from django.core import exceptions


class UserResposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, data):
        user = User(**data)

        password = data.get("password")

        errors = dict()
        try:
            validators.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserRegisterSerializer, self).validate(data)

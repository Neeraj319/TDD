from rest_framework import serializers
from auth.serializers import UserResposeSerializer

from core.models import Blog


class BlogSerializerResponse(serializers.ModelSerializer):
    user = UserResposeSerializer()

    class Meta:
        model = Blog
        fields = "__all__"


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ("written_at", "user")

    def create(self, validated_data):
        blog = Blog.objects.create(**self.data, **validated_data)
        return BlogSerializerResponse(blog)

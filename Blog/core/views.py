from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from core.models import Blog
from core.serializers import BlogCreateSerializer, BlogSerializerResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class BlogViewSet(viewsets.ViewSet):
    queryset = Blog.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        serializer = BlogSerializerResponse(self.queryset, many=True)
        return Response(
            data=serializer.data,
        )

    def retrieve(self, request, pk=None):
        blog = get_object_or_404(self.queryset, pk=pk)
        serializer = BlogSerializerResponse(blog)
        return Response(data=serializer.data)

    def create(self, request):
        blog_seriazlier = BlogCreateSerializer(data=request.data)
        if blog_seriazlier.is_valid():
            blog = blog_seriazlier.create({"user": request.user})
            return Response(data=blog.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=blog_seriazlier.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

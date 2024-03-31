from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from twitter.models import Post
from .serializers import PostSerializers
# Create your views here.


@api_view(['GET'])
def PostListApi(request: Request):
    posts = Post.objects.all()
    posts_serializer = PostSerializers(posts, many=True)
    return Response(posts_serializer.data , status.HTTP_200_OK)
    
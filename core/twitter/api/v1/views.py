from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from twitter.models import Post
from .serializers import PostSerializers
# Create your views here.


@api_view(['GET','POST'])
def PostListApi(request: Request):
    if request.method == 'GET':
        posts = Post.objects.all()
        posts_serializer = PostSerializers(posts, many=True)
        return Response(posts_serializer.data , status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status.HTTP_201_CREATED)
    else:
        return Response(serializer.data , status.HTTP_400_BAD_REQUEST)
         
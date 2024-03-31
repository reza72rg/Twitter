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
         
@api_view(['GET','DELETE','PUT'])     
def PostApiDelete(request : Request, pk: int):
    try:
        post = Post.objects.get(pk = pk)
    except Post.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        post_serializers = PostSerializers(post)
        return Response(post_serializers.data , status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializers = PostSerializers(post, data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data , status.HTTP_202_ACCEPTED)
        return Response(None , status.HTTP_400_BAD_REQUEST)
            
        
    elif request.method == 'DELETE':
        post.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)

        
    
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import mixins, generics
from twitter.models import Post
from .serializers import PostSerializers

# Create your views here.

# region generics
class PostgenericsApiView(generics.ListCreateAPIView):
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    
class PostgenericsDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    
    
#endregion

# region mixins views

class PostMixinsApiView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    
    def get(self, request: Request):
        return self.list(request)
    def post(self, request: Request):
        return self.create(request)

class PostDetailMixinsApiView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin ,generics.GenericAPIView):
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    
    def get(self, request: Request, pk:int):
        return self.retrieve(request, pk)
    def put(self, request: Request, pk:int):
        return self.update(request, pk)
    def delete(self, request: Request, pk:int):
        return self.destroy(request, pk)
    
       
    
# endregion

# region class base views

class PostListAPIView(APIView):
    def get(self, request: Request):
        posts = Post.objects.all()
        posts_serializer = PostSerializers(posts, many=True)
        return Response(posts_serializer.data, status.HTTP_200_OK)
    
    def post(self, request: Request):
        serializer= PostSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    
class PostDetailAPIView(APIView):
    def get_objects(self, pk:int):
        try:
            post = Post.objects.get(pk = pk)
            return post
        except Post.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)
        
    def get(self, request: Request, pk:int):
        post = self.get_objects(pk)
        posts_serializer = PostSerializers(post)
        return Response(posts_serializer.data, status.HTTP_200_OK)
    
    def put(self, request: Request, pk:int):
        post = self.get_objects(pk)
        serializer = PostSerializers(post, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(None, status.HTTP_400_BAD_REQUEST)
    def delete(self, request: Request, pk:int):
        post = self.get_objects(pk)
        post.delete()
        return Response(None, status.HTTP_202_ACCEPTED)
        
# endregion

# region function base views

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

# endregion      
    
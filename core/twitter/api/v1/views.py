from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from twitter.models import Profile, Like, DisLike, Comment
from twitter.models import Post
from .serializers import PostSerializers, UserSerializers, LikeSerializers\
    , DislikeSerializers, CommentSerializers

# Create your views here.


class  PostViewsetsApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    
class  UserViewsetsApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializers    
    
class  LikeViewsetsApiView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers    
    
class  DisLikeViewsetsApiView(viewsets.ModelViewSet):
    queryset = DisLike.objects.all()
    serializer_class = DislikeSerializers    
    
class  CommentViewsetsApiView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers    
    
                     
    
    

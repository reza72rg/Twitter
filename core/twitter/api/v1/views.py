from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from twitter.models import Profile, Like, DisLike, Comment
from twitter.models import Post
from .serializers import PostSerializers, UserSerializers, LikeSerializers\
    , DislikeSerializers, CommentSerializers
from .permission import IsOwnerOrReadOnly
# Create your views here.


class  PostViewsetsApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'archive']
    search_fields = ['content']
    ordering_fields = ['created_date']
    
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
    
                     
    
    

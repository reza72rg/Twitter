from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from twitter.models import Profile, Like, DisLike, Comment
from twitter.models import Post
from .serializers import PostSerializers, UserSerializers, LikeSerializers\
    , DislikeSerializers, CommentSerializers
from .permission import IsOwnerOrReadOnly
from twitter.api.v1.pagination import CustomPagination

# Create your views here.


class  PostViewsetsApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'archive']
    search_fields = ['content']
    ordering_fields = ['created_date']
    pagination_class  = CustomPagination

    # def get_queryset(self, *args, **kwargs):
    #     return (super().get_queryset(*args, **kwargs).filter(author=self.request.user.profile))

  
class  UserViewsetsApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializers  
    
class  UserDetailsViewsetsApiView(generics.RetrieveAPIView):
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
    
                     
    
    

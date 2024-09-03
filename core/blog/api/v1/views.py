from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from blog.models import Profile, Like, DisLike
from blog.models import Post, Category
from .serializers import (
    PostSerializers,
    LikeSerializers,
    DislikeSerializers,
    CategorySerializers,
    PostSerializersArchive,
)
from .permission import IsOwnerOrReadOnly
from blog.api.v1.pagination import CustomPagination
from accounts.models import Follow

# Create your views here.


class PostViewSetsApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # queryset = Post.objects.order_by('created_date').all()
    serializer_class = PostSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author", "category"]
    search_fields = ["content"]
    ordering_fields = ["created_date"]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_follow = Follow.objects.filter(
            user=self.request.user.profile
        ).values_list("follow_user", flat=True)
        queryset = Post.objects.filter(
            author__in=user_follow, archive=True
        ) | Post.objects.filter(author=self.request.user.profile, archive=True)
        return queryset

    # def get_queryset(self, *args, **kwargs):
    #     return (super().get_queryset(*args, **kwargs).filter(author=self.request.user.profile))


class LikeViewSetsApiView(viewsets.ModelViewSet):
    serializer_class = LikeSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        queryset = Like.objects.filter(user=user)
        return queryset


class DisLikeViewSetsApiView(viewsets.ModelViewSet):
    serializer_class = DislikeSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        queryset = DisLike.objects.filter(user=user)
        return queryset


class CategoryViewSetsApiView(viewsets.ModelViewSet):
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()


class PostArchiveListView(generics.ListAPIView):
    serializer_class = PostSerializersArchive
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        queryset = Post.objects.filter(author=user, archive=False)
        return queryset


class PostArchiveDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PostSerializersArchive
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        queryset = Post.objects.filter(author=user, archive=False)
        return queryset

from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.models import Follow
from .serializers import FollowersSerializers
from accounts.models import Profile


class  FollowersViewsetsApiView(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializers    
    
                     

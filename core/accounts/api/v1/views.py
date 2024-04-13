from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.models import Follow
from .serializers import FollowersSerializers, UserSerializers, Registerserializer
from accounts.models import Profile
from rest_framework import viewsets
from rest_framework import status

class  FollowersViewsetsApiView(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowersSerializers    
    
                     
class  UserViewsetsApiView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializers  
    

class RegisterViewsetsApiView(generics.GenericAPIView):
    serializer_class = Registerserializer
    def post(self,request,*args,**kwargs):
        serializer = Registerserializer(data = request.data)
        if serializer.is_valid():
            data = {
                'email': serializer.validated_data['email']
            }
           
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
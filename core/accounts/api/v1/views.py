from rest_framework import  generics
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from accounts.models import Follow
from .serializers import FollowersSerializers, ProfileSerializers, Registerserializer\
    ,CustomTokenSerializer, CustomAuthTokenSerializer, ChangePasswordSerializer\
        ,LoginSerializer , ActivateResendSerializer
from accounts.models import Profile
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from ..utils import EmailThread
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
   
class  FollowersViewsetsApiView(viewsets.ModelViewSet):
    # queryset = Follow.objects.all()
    serializer_class = FollowersSerializers  
    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user.profile) 
        return queryset  
class  FollowingViewsetsApiView(generics.ListAPIView):
    serializer_class = FollowersSerializers 
    def get_queryset(self):
        queryset = Follow.objects.filter(follow_user = self.request.user.profile)
        return queryset     
                     
class  ProfileViewsetsApiView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user = self.request.user)
        return obj
    
    
class RegisterViewsetsApiView(generics.GenericAPIView):
    serializer_class = Registerserializer
    def post(self,request,*args,**kwargs):
        serializer = Registerserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user_name = serializer.validated_data['username']
            data = {
                'username': user_name
            }
            user_obj = get_object_or_404(User, username = user_name)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation.tpl', {'token': token}, 'reza72rg@gmail.com',to=['test.@gmail.com'])
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def get_tokens_for_user(self, user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)



class CustomLoginAuthToken(ObtainAuthToken):
    serializer_class = CustomTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
        
class CustomLogoutAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomAuthTokenSerializer
    
    
    
class ChangePasswordViewsetsApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password was change successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginApiView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Login view to get user credentials
        """
        serializer = LoginSerializer(data=request.data, many=False)

        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            if user is not None and user.is_active:
                login(request, user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestEmail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        self.email = 'reza72@email.com'
        user_obj = get_object_or_404(User, email = self.email)
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'reza72rg@gmail.com',to=['test.@gmail.com'])
        EmailThread(email_obj).start()
        return Response("Send email successful")
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)





class ActivationApiView(APIView):
    def get(self, request,token, *args, **kwargs):
        try:
            token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get('user_id') 
            user_obj = Profile.objects.get(pk = user_id)
            if not user_obj.is_verified:
                user_obj.is_verified = True
                user_obj.save()
                return Response(
                    {"username": "Successfully activated"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Your accounts already been verified"},
                    status=status.HTTP_200_OK,
                )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activations link expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid Token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivateResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = ActivateResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_object)
        email_obj = EmailMessage(
            "email/activation.tpl",
            {"token": token},
            "reza72rg@gmail.com",
            to=[user_object.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "Email activate resend successfully"},
            status=status.HTTP_200_OK,
        )
       
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
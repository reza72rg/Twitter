from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    CustomTokenObtainPairView,
    FollowersViewsetsApiView,
    UserViewsetsApiView,
    RegisterViewsetsApiView,
    CustomLoginAuthToken,
    CustomLogoutAuthToken,
    
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewsetsApiView, basename="followers")


urlpatterns = [
    path('api-token/login/', CustomLoginAuthToken.as_view(), name= "token-login"),
    path('api-token/logout/', CustomLogoutAuthToken.as_view(), name= "token-logout"),
    path("register/", RegisterViewsetsApiView.as_view(), name= "register-users"),
    path("users/", UserViewsetsApiView.as_view(), name= "task-users"),
    
    path('token-jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ router.urls


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
    ProfileViewsetsApiView,
    RegisterViewsetsApiView,
    CustomLoginAuthToken,
    CustomLogoutAuthToken,
    ChangePasswordViewsetsApiView,
    LoginApiView,
    #LogoutApiView,
    FollowingViewsetsApiView,
    TestEmail,
    ActivationApiView,
    ActivationResendApiView,
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewsetsApiView, basename="followers")


urlpatterns = [
    path("test/",TestEmail.as_view(),name="test"),
    # following
    path("following/", FollowingViewsetsApiView.as_view(), name="following"),
    
    # login user
    path("login/", LoginApiView.as_view(), name="login"),
    #path("logout/", LogoutApiView.as_view(), name="logout"),
    
    # activation
    path("activation/confirm/<str:token>/",ActivationApiView.as_view(),name="activation",),
    path("activation/resend/",ActivationResendApiView.as_view(),name="resend-activation",),
    
    path("profile/", ProfileViewsetsApiView.as_view(), name= "profile-user"),
    # Change password
    path("change-password/", ChangePasswordViewsetsApiView.as_view(), name= "changepassword-users"),
    # Registrations
    path("register/", RegisterViewsetsApiView.as_view(), name= "register-users"),
   
    # Login Token
    path('api-token/login/', CustomLoginAuthToken.as_view(), name= "token-login"),
    path('api-token/logout/', CustomLogoutAuthToken.as_view(), name= "token-logout"),
    
    # Login JWT
    path('token-jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ router.urls


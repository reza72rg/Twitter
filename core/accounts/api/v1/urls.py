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
    FollowersViewSetsApiView,
    ProfileViewSetsApiView,
    RegisterViewSetsApiView,
    CustomLoginAuthToken,
    CustomLogoutAuthToken,
    ChangePasswordViewSetsApiView,
    LoginApiView,
    LogoutApiView,
    FollowingViewSetsApiView,
    TestEmail,
    ActivationApiView,
    ActivationResendApiView,
    ResetPasswordApiView,
    ResetPasswordConfirmApiView,
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewSetsApiView, basename="followers")


urlpatterns = [
    path("test/", TestEmail.as_view(),name="test"),
    # following
    path("following/", FollowingViewSetsApiView.as_view(), name="following"),
    
    # login user
    path("login/", LoginApiView.as_view(), name="login"),
    path("logout/", LogoutApiView.as_view(), name="logout"),
    
    # activation
    path("activation/confirm/<str:token>/", ActivationApiView.as_view(), name="activation",),
    path("activation/resend/", ActivationResendApiView.as_view(), name="resend-activation",),
   
    path("profile/", ProfileViewSetsApiView.as_view(), name="profile-user"),
    # Change password
    path("change-password/", ChangePasswordViewSetsApiView.as_view(), name="changepassword-users"),
    # Reset Password
    path("send-reset-password-link/",ResetPasswordApiView.as_view(), name="resetpassword",),
    path("reset-password/<str:token>/",ResetPasswordConfirmApiView.as_view(), name="resetpassword-confirm",),
    
    # Registrations
    path("register/", RegisterViewSetsApiView.as_view(), name="register-users"),
   
    # Login Token
    path('api-token/login/', CustomLoginAuthToken.as_view(), name="token-login"),
    path('api-token/logout/', CustomLogoutAuthToken.as_view(), name="token-logout"),
    
    # Login JWT
    path('token-jwt/create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token-jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]+ router.urls



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import (
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
]+ router.urls


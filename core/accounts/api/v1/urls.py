from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import (
    FollowersViewsetsApiView,
    UserViewsetsApiView,
    RegisterViewsetsApiView,
    CustomAuthToken,
    
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewsetsApiView, basename="followers")


urlpatterns = [
    path('api-token/', CustomAuthToken.as_view()),
    path("register/", RegisterViewsetsApiView.as_view(), name= "register-users"),
    path("users/", UserViewsetsApiView.as_view(), name= "task-users"),
]+ router.urls


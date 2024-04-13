from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FollowersViewsetsApiView,
    UserViewsetsApiView,
    RegisterViewsetsApiView,
    
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewsetsApiView, basename="followers")


urlpatterns = [
    path("register/", RegisterViewsetsApiView.as_view(), name= "register-users"),
    path("users/", UserViewsetsApiView.as_view(), name= "task-users"),
]+ router.urls


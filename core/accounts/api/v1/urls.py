from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FollowersViewsetsApiView,
    
)
app_name = "api-v1"

router = DefaultRouter()
router.register("followers", FollowersViewsetsApiView, basename="followers")


urlpatterns = router.urls

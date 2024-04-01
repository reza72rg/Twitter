from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewsetsApiView,
    UserViewsetsApiView,
    LikeViewsetsApiView,
    DisLikeViewsetsApiView,
    CommentViewsetsApiView,
)
app_name = "api-v1"

router = DefaultRouter()
router.register("task", PostViewsetsApiView, basename="task")
router.register("like", LikeViewsetsApiView, basename="like")
router.register("dislike", DisLikeViewsetsApiView, basename="dislike")
router.register("comment", CommentViewsetsApiView, basename="comment")

urlpatterns = [
    path("users/", UserViewsetsApiView.as_view(), name= "task-users"),
] + router.urls


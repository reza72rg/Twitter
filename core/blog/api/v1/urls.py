from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSetsApiView,
    LikeViewSetsApiView,
    DisLikeViewSetsApiView,
    CategoryViewSetsApiView,
    PostArchiveListView,
    PostArchiveDetailView,
    
    )
app_name = "api-v1"

router = DefaultRouter()
router.register("task", PostViewSetsApiView, basename="task")
router.register("like", LikeViewSetsApiView, basename="like")
router.register("dislike", DisLikeViewSetsApiView, basename="dislike")

router.register("category", CategoryViewSetsApiView, basename="category")

urlpatterns = [
    path("task-archive/", PostArchiveListView.as_view(), name="task-archive"),
    path("task-archive/<int:pk>/", PostArchiveDetailView.as_view(), name="task-archive-update")
    ]+router.urls


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostListApi,
    PostApiDelete,
    PostListAPIView,
    PostDetailAPIView,
    PostMixinsApiView,
    PostDetailMixinsApiView,
    PostgenericsApiView,
    PostgenericsDetailApiView,
    PostViewsetsApiView,
    UserViewsetsApiView,
)

router = DefaultRouter()
router.register('',PostViewsetsApiView)
urlpatterns = [
    path("task/", PostListApi, name= "task-list"),
    path("task/<int:pk>/", PostApiDelete, name= "task-delete"),
    path("cbv/", PostListAPIView.as_view(), name= "task-list_cbv"),
    path("cbv/<int:pk>/", PostDetailAPIView.as_view(), name= "task-list_cbv"),
    path("mixins/", PostMixinsApiView.as_view(), name= "task-list_mixins"),
    path("mixins/<int:pk>/", PostDetailMixinsApiView.as_view(), name= "task-list_mixins"),
    path("generics/", PostgenericsApiView.as_view(), name= "task-list_generics"),
    path("generics/<int:pk>/", PostgenericsDetailApiView.as_view(), name="task-list_generics"),
    path("users/", UserViewsetsApiView.as_view(), name= "task-users"),
    path("viewsets/", include(router.urls)),
    
]

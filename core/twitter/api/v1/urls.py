from django.urls import path
from .views import (
    PostListApi,
    PostApiDelete,
    PostListAPIView,
    PostDetailAPIView,
)


urlpatterns = [
    path("task/",PostListApi,name="task-list"),
    path("task/<int:pk>/",PostApiDelete,name="task-delete"),
    path("task/cbv/",PostListAPIView.as_view(),name="task-list_cbv"),
    path("task/cbv/<int:pk>/",PostDetailAPIView.as_view(),name="task-list_cbv"),
]

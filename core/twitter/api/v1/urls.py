from django.urls import path
from .views import (
    PostListApi,
    PostApiDelete,
)


urlpatterns = [
    path("task/",PostListApi,name="task-list"),
    path("task/<int:pk>/",PostApiDelete,name="task-delete"),
]
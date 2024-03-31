from django.urls import path
from .views import (
    PostListApi,
)


urlpatterns = [
    path("task/",PostListApi,name="task-list"),
]
from django.urls import path
from .views import (
    PostListApi,
    PostApiDelete,
    PostListAPIView,
    PostDetailAPIView,
    PostMixinsApiView,
    PostDetailMixinsApiView,
    PostgenericsApiView,
    PostgenericsDetailApiView,
)


urlpatterns = [
    path("task/",PostListApi,name="task-list"),
    path("task/<int:pk>/",PostApiDelete,name="task-delete"),
    path("cbv/",PostListAPIView.as_view(),name="task-list_cbv"),
    path("cbv/<int:pk>/",PostDetailAPIView.as_view(),name="task-list_cbv"),
    path("mixins/",PostMixinsApiView.as_view(),name="task-list_mixins"),
    path("mixins/<int:pk>/",PostDetailMixinsApiView.as_view(),name="task-list_mixins"),
    path("generics/",PostgenericsApiView.as_view(),name="task-list_generics"),
    path("generics/<int:pk>/",PostgenericsDetailApiView.as_view(),name="task-list_generics"),
]

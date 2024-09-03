from django.urls import path, include
from blog.views import (
    UserCreatePostView,
    PostListView,
    Aboutpage,
    FollowersView,
    UserFollowListView,
    DeletePostView,
    UpdatePostView,
    DetailsPostView,
    FollowUserView,
    LikePostView,
    DisLikePostView,
    ArchivePostsView,
)

# Set the app name for namespacing
app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home_page"),
    path("about/", Aboutpage.as_view(), name="about"),
    path(
        "all-post-archive/", ArchivePostsView.as_view(), name="archive_posts"
    ),
    path(
        "user/<int:user_id>", UserFollowListView.as_view(), name="user-follows"
    ),
    path("create_post/", UserCreatePostView.as_view(), name="create-posts"),
    path(
        "followers/<int:user_id>/<str:letter>",
        FollowersView.as_view(),
        name="user-followers",
    ),
    path("delete/<int:pk>/", DeletePostView.as_view(), name="delete"),
    path("edit/<int:pk>/", UpdatePostView.as_view(), name="update_post"),
    path("details/<int:pk>/", DetailsPostView.as_view(), name="details_post"),
    path("search/", PostListView.as_view(), name="search"),
    path("follow/", FollowUserView.as_view(), name="follow"),
    path("like/<int:pk>/", LikePostView.as_view(), name="like-post"),
    path("dislike/<int:pk>/", DisLikePostView.as_view(), name="dislike-post"),
    path("blog/api/v1/", include("blog.api.v1.urls")),
]

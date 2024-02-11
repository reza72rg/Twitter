from django.urls import path, include
from twitter.views import UserCreatePostView, PostListView, Aboutpage, FollowersView, UserFollowListView

# Set the app name for namespacing
app_name = "twitter"

urlpatterns = [
    path(
        "",PostListView.as_view(),name= "home_page"
    ),
    path(
        "about/",Aboutpage.as_view(),name="about"
    ),
    path('user/<int:user_id>', UserFollowListView.as_view(), name='user-follows'),
    path('create_post/', UserCreatePostView.as_view(), name='create-posts'),
    path('followers/<int:user_id>/<str:letter>', FollowersView.as_view(), name='user-followers'),
    #path('following/<int:user_id>', FollowingView.as_view(), name='user-following'),



]
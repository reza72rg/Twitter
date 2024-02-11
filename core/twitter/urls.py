from django.urls import path, include
from twitter.views import UserPostListView, PostListView, Aboutpage, FollowersView

# Set the app name for namespacing
app_name = "twitter"

urlpatterns = [
    path(
        "",PostListView.as_view(),name= "home_page"
    ),
    path(
        "about/",Aboutpage.as_view(),name="about"
    ),
    path('user/<int:user_id>', UserPostListView.as_view(), name='user-follows'),
    path('followers/<int:user_id>/<str:letter>', FollowersView.as_view(), name='user-followers'),
    #path('following/<int:user_id>', FollowingView.as_view(), name='user-following'),



]
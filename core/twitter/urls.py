from django.urls import path, include
from twitter.views import UserPostListView, PostListView, Aboutpage

# Set the app name for namespacing
app_name = "twitter"

urlpatterns = [
    path(
        "",PostListView.as_view(),name= "home_page"
    ),
    path(
        "about/",Aboutpage.as_view(),name="about"
    ),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

]
from django.urls import path, include
from twitter.views import *

# Set the app name for namespacing
app_name = "twitter"

urlpatterns = [
    path(
        "",HomeView.as_view(),name= "home_page"
    ),
    path(
        "about/",Aboutpage.as_view(),name="about"
    ),

]
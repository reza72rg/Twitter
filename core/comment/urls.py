from django.urls import path, include
from comment.views import *


# Set the app name for namespacing
app_name = "comment"

urlpatterns = [
    path("comment/api/v1/", include("comment.api.v1.urls")),
    ]

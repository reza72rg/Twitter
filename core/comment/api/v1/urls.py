from rest_framework.routers import DefaultRouter
from .views import CommentViewSetsApiView


app_name = "api-v1"

router = DefaultRouter()
router.register("comment", CommentViewSetsApiView, basename="comment")
urlpatterns = router.urls

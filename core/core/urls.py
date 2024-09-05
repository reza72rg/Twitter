from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
    openapi.Info(
        title="Twitter API",
        default_version="v1",
        description="this is a test api for Twitter Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="reza72rg@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api-auth/", include("rest_framework.urls")),
        path("logout/", auth_views.LogoutView.as_view(), name="logout"),
        path("", include("blog.urls")),
        path("accounts/", include("accounts.urls")),
        path("comment/", include("comment.urls")),
        path(
            "swagger/output.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

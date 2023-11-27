from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven API",
        default_version="v1",
        description="API endpoints for Authors Haven API Class",
        contact=openapi.Contact(email="marilynjmarquez@gmail.com"),
        license=openapi.License(name="MIT")
    ),
    public=True,
    permission_classes=(permissions.AllowAny),
)
urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
]

admin.site.site_header = "Authors Haven API Admin"
admin.site.site_title = "Authors Haven API Admin Portal"
admin.site.index_title = "Welcome to Authors Have API Portal"

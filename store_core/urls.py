"""
store_core URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

try:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    from payments.views import CreatePaymentIntentView

    urlpatterns += [
        path("api/", include("store_core.api_router")),
        path("api/payments/create-intent/", CreatePaymentIntentView.as_view(), name="create-payment-intent"),
    ]

    api_info = openapi.Info(
        title="E-Commerce Store API",
        default_version="v1",
        description="Full API documentation for E-Commerce Store Platform",
    )

    schema_view = get_schema_view(
        api_info,
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
    ]
except ImportError:
    pass

admin.site.site_header = "E-Commerce Store Admin"
admin.site.site_title = "E-Commerce Store Portal"
admin.site.index_title = "Store Administration"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin
from django.urls import include, path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Product API',
        default_version='0.1',
        description='Simple API for inventory purposes.',
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('catalog.urls')),
    path('api/', include('catalog_auth.urls')),
    path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/docs', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



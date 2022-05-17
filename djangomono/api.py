from django.urls import path, re_path
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Djagno Coffe Api",
        default_version='v1',
        description="Best coffe app! Enjoy!",
        terms_of_service="https://www.sylwesterwalczak.pl",
        contact=openapi.Contact(email="me@sylwesterwalczak.pl"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('authx/', include('authx.urls')),
    path('supplier/', include('supplier.urls')),
    path('story/', include('story.urls')),
    path('menu/', include('menu.urls')),
    path('purchase/', include('purchase.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_v1.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_v1.with_ui('redoc',
            cache_timeout=0), name='schema-redoc')
]

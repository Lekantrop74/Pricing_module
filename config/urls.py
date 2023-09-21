from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from Pricing_marketplace_module.views import CalculatePriceView

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf/users/', include("users.urls", namespace="users")),
    path('calculate_price/', include('Pricing_marketplace_module.urls', namespace='Pricing_marketplace_module')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]

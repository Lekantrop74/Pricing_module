from django.urls import path

from Pricing_marketplace_module.views import CalculatePriceView


app_name = "Pricing_marketplace_module"


urlpatterns = [
    path('', CalculatePriceView.as_view(), name='calculate_price'),
]



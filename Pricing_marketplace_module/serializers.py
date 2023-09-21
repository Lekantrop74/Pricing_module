from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Pricing_marketplace_module.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

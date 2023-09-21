from django.contrib import admin

from Pricing_marketplace_module.models import Product


# Register your models here.
@admin.register(Product)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name"]
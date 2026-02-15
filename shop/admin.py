from django.contrib import admin
from .models import Product, Purchase, PurchaseItem, Denomination, DenominationCount


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_id", "available_stocks", "price", "tax_percentage")
    search_fields = ("name", "product_id")
    list_filter = ("tax_percentage",)


@admin.register(Denomination)
class DenominationAdmin(admin.ModelAdmin):
    list_display = ("value",)
    ordering = ("value",)


from django.contrib import admin

from models import Merchant, Product, ProductComparison


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "price", "stock")


@admin.register(ProductComparison)
class ProductComparisonAdmin(admin.ModelAdmin):
    list_display = ("seller", "name", "status", "current_price", "last_modified")
    search_fields = ("name", )

    def status(self, obj):
        if obj.is_on_promotion():
            return "PROMO"
        return ""

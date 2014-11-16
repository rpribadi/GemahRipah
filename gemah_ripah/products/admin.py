from django.contrib import admin

from models import Brand, Product, Comparison


admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "price", "stock")

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ("seller", "product", "status", "current_price", "last_update")
    search_fields = ("product", )

    def status(self, obj):
        if obj.is_on_promotion():
            return "PROMO"
        return ""

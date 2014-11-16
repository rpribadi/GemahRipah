from django.contrib import admin

from models import Brand, Product


admin.site.register(Brand)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "price", "stock")
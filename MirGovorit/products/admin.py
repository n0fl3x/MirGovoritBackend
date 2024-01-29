from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('use_count',)


admin.site.register(Product, ProductAdmin)

from django.contrib import admin


# Register your models here.
from logistic.models import Stock, StockProduct, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description']


class StockProductInline(admin.TabularInline):
    model = StockProduct
    fields = ['product', 'quantity', 'price']
    extra = 3


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['address', 'id']
    inlines = [StockProductInline, ]

from django.contrib import admin
from .models import Livestock, Product

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ('name', 'health_status', 'breed')
    search_fields = ('name', 'breed')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category')

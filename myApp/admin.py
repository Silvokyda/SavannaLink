from django.contrib import admin
from .models import Livestock

@admin.register(Livestock)
class LivestockAdmin(admin.ModelAdmin):
    list_display = ('name', 'health_status', 'breed')
    search_fields = ('name', 'breed')
   

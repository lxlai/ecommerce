from django.contrib import admin

# Register your models here.

from items.models import Item, Order

class ItemAdmin(admin.ModelAdmin):
	fields = ['name', 'description', 'price']

class OrderAdmin(admin.ModelAdmin):
	fields = ['status', 'user']

admin.site.register(Item)
admin.site.register(Order)
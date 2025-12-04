from django.contrib import admin
from .models import Product, Order, OrderItem

# Register your models here.
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price')
    inlines = [OrderItemInline]

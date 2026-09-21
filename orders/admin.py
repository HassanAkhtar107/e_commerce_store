from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "price", "quantity", "subtotal"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "email", "total_amount", "payment_status", "order_status", "created_at"]
    list_filter = ["order_status", "payment_status", "created_at"]
    search_fields = ["order_number", "full_name", "email"]
    inlines = [OrderItemInline]

from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity", "subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "user", "full_name", "email",
            "phone_number", "shipping_address_text", "total_amount",
            "payment_method", "payment_status", "order_status", "stripe_payment_intent_id",
            "items", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "order_number", "created_at", "updated_at"]

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff or self.request.user.user_type == "ADMIN":
                return Order.objects.all()
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    @action(detail=False, methods=["post"])
    def create_order(self, request):
        user = request.user if request.user.is_authenticated else None
        full_name = request.data.get("full_name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number", "")
        shipping_address_text = request.data.get("shipping_address_text")
        payment_method = request.data.get("payment_method", "COD")

        if not full_name or not email or not shipping_address_text:
            return Response({"error": "Full name, email, and shipping address are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve user cart or session cart
        if user:
            cart = Cart.objects.filter(user=user).first()
        else:
            session_id = request.headers.get("X-Session-ID") or request.session.session_key
            cart = Cart.objects.filter(session_id=session_id).first()

        if not cart or cart.items.count() == 0:
            return Response({"error": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            shipping_address_text=shipping_address_text,
            total_amount=cart.total_price,
            payment_method=payment_method,
            payment_status="PENDING",
            order_status="PENDING"
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.current_price,
                quantity=cart_item.quantity
            )
            # Update product stock safely
            if cart_item.product.stock >= cart_item.quantity:
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()

        # Clear cart after creating order
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def dashboard_stats(self, request):
        total_products = Product.objects.count()
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(order_status="PENDING").count()
        completed_orders = Order.objects.filter(order_status="DELIVERED").count()
        total_customers = User.objects.count()

        recent_orders = OrderSerializer(Order.objects.all()[:5], many=True).data

        return Response({
            "total_products": total_products,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "total_customers": total_customers,
            "recent_orders": recent_orders
        }, status=status.HTTP_200_OK)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.AllowAny]

    def _get_or_create_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            return cart
        session_id = request.headers.get("X-Session-ID") or request.session.session_key
        if not session_id:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
        return cart

    def list(self, request, *args, **kwargs):
        cart = self._get_or_create_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self._get_or_create_cart(request)
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found or unavailable"}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def update_item(self, request):
        cart = self._get_or_create_cart(request)
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        cart = self._get_or_create_cart(request)
        item_id = request.data.get("item_id")

        CartItem.objects.filter(id=item_id, cart=cart).delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        cart = self._get_or_create_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

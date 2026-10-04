from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Brand, Product, ProductImage, Review
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer,
    ProductImageSerializer, ReviewSerializer
)


# ─── Custom permission for admin-only endpoints ───────────────────────────────

class IsAdminUser(permissions.BasePermission):
    """Allow access only to users with ADMIN user_type or is_staff."""
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_staff or getattr(request.user, "user_type", None) == "ADMIN")
        )


# ─── Category ─────────────────────────────────────────────────────────────────

class CategoryViewSet(viewsets.ModelViewSet):
    """Public: only active categories."""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ─── Brand ────────────────────────────────────────────────────────────────────

class BrandViewSet(viewsets.ModelViewSet):
    """Public: all brands."""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ─── User-Facing Product Endpoint ─────────────────────────────────────────────

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    PUBLIC endpoint — always returns ONLY active (is_available=True) products.
    This is used by the storefront. No admin writes allowed here.
    """
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["gender", "category__slug", "brand__slug", "is_featured"]
    search_fields = ["name", "description", "short_description", "category__name"]
    ordering_fields = ["price", "created_at", "rating"]

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def add_review(self, request, slug=None):
        product = self.get_object()
        rating = request.data.get("rating", 5)
        comment = request.data.get("comment", "")
        review = Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        reviews = product.reviews.all()
        product.num_reviews = reviews.count()
        product.rating = sum([r.rating for r in reviews]) / max(product.num_reviews, 1)
        product.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


# ─── Admin-Only Product Endpoint ──────────────────────────────────────────────

class AdminProductViewSet(viewsets.ModelViewSet):
    """
    ADMIN-ONLY endpoint — returns ALL products regardless of is_available status.
    Allows admins to create, update, delete, and toggle product availability.
    Requires admin authentication on every request.
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["gender", "category__slug", "brand__slug", "is_featured", "is_available"]
    search_fields = ["name", "description", "short_description", "category__name"]
    ordering_fields = ["price", "created_at", "rating", "is_available"]

    @action(detail=True, methods=["patch"])
    def toggle_availability(self, request, slug=None):
        """Toggle is_available on/off for a product."""
        product = self.get_object()
        product.is_available = not product.is_available
        product.save()
        return Response(
            {
                "id": product.id,
                "slug": product.slug,
                "name": product.name,
                "is_available": product.is_available,
            },
            status=status.HTTP_200_OK,
        )

from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Brand, Product, ProductImage, Review
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer,
    ProductImageSerializer, ReviewSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category__slug", "brand__slug", "is_featured"]
    search_fields = ["name", "description", "short_description"]
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
        # Update product average rating
        reviews = product.reviews.all()
        product.num_reviews = reviews.count()
        product.rating = sum([r.rating for r in reviews]) / max(product.num_reviews, 1)
        product.save()
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, Review


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_feature"]


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "image", "is_active", "product_count"]

    def get_product_count(self, obj):
        return obj.products.filter(is_available=True).count()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "logo", "description"]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        model = Review
        fields = ["id", "product", "user", "user_name", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    brand_detail = BrandSerializer(source="brand", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "sku", "category", "category_detail",
            "brand", "brand_detail", "gender", "description", "short_description",
            "price", "discount_price", "current_price", "discount_percentage", "stock",
            "is_available", "is_featured", "rating", "num_reviews",
            "images", "reviews", "created_at", "updated_at"
        ]

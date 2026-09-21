from django.core.management.base import BaseCommand
from products.models import Category, Brand, Product, ProductImage


class Command(BaseCommand):
    help = "Seeds the database with initial e-commerce categories, brands, and products."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding E-Commerce Data...")

        # Categories
        cat_electronics, _ = Category.objects.get_or_create(
            name="Electronics",
            defaults={"description": "High-tech gadgets, headphones, smartwatches, and gear.", "is_active": True}
        )
        cat_fashion, _ = Category.objects.get_or_create(
            name="Fashion & Apparel",
            defaults={"description": "Trending clothing, sneakers, jackets, and streetwear.", "is_active": True}
        )
        cat_home, _ = Category.objects.get_or_create(
            name="Home & Lifestyle",
            defaults={"description": "Modern furniture, lamps, coffee makers, and decor.", "is_active": True}
        )
        cat_fitness, _ = Category.objects.get_or_create(
            name="Sports & Fitness",
            defaults={"description": "Smart trackers, gym equipment, yoga mats, and bottles.", "is_active": True}
        )

        # Brands
        brand_nexus, _ = Brand.objects.get_or_create(name="Nexus Audio")
        brand_urban, _ = Brand.objects.get_or_create(name="Urban Thread")
        brand_luxe, _ = Brand.objects.get_or_create(name="LuxeLiving")

        # Products
        products_data = [
            {
                "name": "Nexus Pro Wireless Headphones",
                "category": cat_electronics,
                "brand": brand_nexus,
                "price": 199.99,
                "discount_price": 149.99,
                "stock": 25,
                "is_featured": True,
                "description": "Active Noise Cancelling over-ear wireless headphones with 40-hour battery life and spatial audio.",
                "short_description": "Premium ANC wireless headphones with studio clarity.",
                "rating": 4.8,
                "num_reviews": 32,
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Urban Minimalist Bomber Jacket",
                "category": cat_fashion,
                "brand": brand_urban,
                "price": 129.00,
                "discount_price": 89.00,
                "stock": 18,
                "is_featured": True,
                "description": "Water-resistant sleek bomber jacket featuring insulated fleece lining and premium brass zippers.",
                "short_description": "Stylish, weather-resistant streetwear jacket.",
                "rating": 4.6,
                "num_reviews": 19,
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Luxe Ambient Ceramic Desk Lamp",
                "category": cat_home,
                "brand": brand_luxe,
                "price": 89.50,
                "discount_price": None,
                "stock": 12,
                "is_featured": True,
                "description": "Hand-crafted matte ceramic table lamp with warm LED light dimming and touch controls.",
                "short_description": "Handcrafted ceramic lamp with touch dimmer.",
                "rating": 4.9,
                "num_reviews": 14,
                "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Smart Fitness & Health Watch Ultra",
                "category": cat_fitness,
                "brand": brand_nexus,
                "price": 249.99,
                "discount_price": 199.99,
                "stock": 30,
                "is_featured": True,
                "description": "AMOLED touch display smart watch with heart rate tracking, GPS route tracing, and 5ATM water resistance.",
                "short_description": "Rugged fitness watch with GPS and health sensors.",
                "rating": 4.7,
                "num_reviews": 45,
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Retro Leather Sneakers",
                "category": cat_fashion,
                "brand": brand_urban,
                "price": 110.00,
                "discount_price": 95.00,
                "stock": 40,
                "is_featured": False,
                "description": "Full-grain white leather low-top sneakers with cushioned arch support and gum outsole.",
                "short_description": "Classic low-top leather sneakers for daily comfort.",
                "rating": 4.5,
                "num_reviews": 22,
                "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Aroma Espresso Machine Pro",
                "category": cat_home,
                "brand": brand_luxe,
                "price": 349.00,
                "discount_price": 299.00,
                "stock": 8,
                "is_featured": False,
                "description": "15-bar Italian pressure pump espresso maker with integrated milk frother wand and PID temperature control.",
                "short_description": "Barista-grade espresso machine for home brewing.",
                "rating": 4.9,
                "num_reviews": 28,
                "image_url": "https://images.unsplash.com/photo-1517668808822-9e428d697818?w=800&auto=format&fit=crop&q=80"
            }
        ]

        for p_data in products_data:
            image_url = p_data.pop("image_url")
            product, created = Product.objects.get_or_create(
                name=p_data["name"],
                defaults=p_data
            )
            if created:
                ProductImage.objects.create(
                    product=product,
                    alt_text=product.name,
                    is_feature=True
                )

        self.stdout.write(self.style.SUCCESS("E-Commerce seed data successfully created!"))

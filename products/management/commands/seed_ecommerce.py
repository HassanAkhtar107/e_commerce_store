from django.core.management.base import BaseCommand
from products.models import Category, Brand, Product, ProductImage


class Command(BaseCommand):
    help = "Seeds the database with Clothing & Footwear categories, brands, and products for Men and Women."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Clothing & Footwear E-Commerce Data...")

        # Categories
        cat_dresses, _ = Category.objects.get_or_create(
            name="Dresses",
            defaults={"description": "Elegant women's dresses, evening gowns, and midi dresses.", "is_active": True}
        )
        cat_shirts, _ = Category.objects.get_or_create(
            name="Shirts",
            defaults={"description": "Formal and casual button-down shirts for men and women.", "is_active": True}
        )
        cat_tshirts, _ = Category.objects.get_or_create(
            name="T-Shirts",
            defaults={"description": "Premium cotton crewnecks, graphic tees, and oversized t-shirts.", "is_active": True}
        )
        cat_pants, _ = Category.objects.get_or_create(
            name="Pants",
            defaults={"description": "Denim jeans, cargo pants, and casual chinos.", "is_active": True}
        )
        cat_trousers, _ = Category.objects.get_or_create(
            name="Trousers",
            defaults={"description": "Tailored formal trousers and pleated trousers.", "is_active": True}
        )
        cat_suits, _ = Category.objects.get_or_create(
            name="Suits",
            defaults={"description": "Three-piece formal tuxedos, blazers, and pant suits.", "is_active": True}
        )
        cat_kurta, _ = Category.objects.get_or_create(
            name="Kurta Pajama",
            defaults={"description": "Traditional ethnic Kurta Pajama sets for celebrations.", "is_active": True}
        )
        cat_shoes, _ = Category.objects.get_or_create(
            name="Shoes",
            defaults={"description": "Leather dress shoes, sneakers, boots, and heels.", "is_active": True}
        )

        # Brands
        brand_royal, _ = Brand.objects.get_or_create(name="Royal Couture")
        brand_urban, _ = Brand.objects.get_or_create(name="Urban Thread")
        brand_heritage, _ = Brand.objects.get_or_create(name="Heritage Ethnic")
        brand_sole, _ = Brand.objects.get_or_create(name="SoleCraft")

        # Products
        products_data = [
            # MEN PRODUCTS
            {
                "name": "Men's Royal Silk Kurta Pajama Set",
                "category": cat_kurta,
                "brand": brand_heritage,
                "gender": "MEN",
                "price": 120.00,
                "discount_price": 95.00,
                "stock": 30,
                "is_featured": True,
                "description": "Handcrafted dupion silk Kurta Pajama set with subtle embroidery on collar and cuffs.",
                "short_description": "Traditional silk Kurta Pajama set for men.",
                "rating": 4.9,
                "num_reviews": 28,
                "image_url": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Men's Premium Oxford Formal Shirt",
                "category": cat_shirts,
                "brand": brand_urban,
                "gender": "MEN",
                "price": 65.00,
                "discount_price": 49.99,
                "stock": 45,
                "is_featured": True,
                "description": "100% Egyptian cotton slim-fit formal shirt with spread collar.",
                "short_description": "Classic formal Oxford button-down shirt.",
                "rating": 4.7,
                "num_reviews": 34,
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Men's Tailored Two-Piece Navy Suit",
                "category": cat_suits,
                "brand": brand_royal,
                "gender": "MEN",
                "price": 350.00,
                "discount_price": 280.00,
                "stock": 15,
                "is_featured": True,
                "description": "Italian wool blend 2-piece notch lapel navy suit with tapered trousers.",
                "short_description": "Italian wool blend suit for business & weddings.",
                "rating": 4.8,
                "num_reviews": 20,
                "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Men's Heritage Genuine Leather Oxford Shoes",
                "category": cat_shoes,
                "brand": brand_sole,
                "gender": "MEN",
                "price": 160.00,
                "discount_price": 129.00,
                "stock": 25,
                "is_featured": True,
                "description": "Hand-stitched burnished calfskin leather Oxford dress shoes with cushioned footbed.",
                "short_description": "Handcrafted leather Oxford dress shoes.",
                "rating": 4.9,
                "num_reviews": 42,
                "image_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Men's Heavyweight Oversized Graphic T-Shirt",
                "category": cat_tshirts,
                "brand": brand_urban,
                "gender": "MEN",
                "price": 40.00,
                "discount_price": 29.99,
                "stock": 60,
                "is_featured": False,
                "description": "240 GSM organic cotton drop-shoulder streetwear graphic t-shirt.",
                "short_description": "Oversized heavy cotton streetwear tee.",
                "rating": 4.6,
                "num_reviews": 18,
                "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800&auto=format&fit=crop&q=80"
            },

            # WOMEN PRODUCTS
            {
                "name": "Women's Floral Silk Wrap Midi Dress",
                "category": cat_dresses,
                "brand": brand_royal,
                "gender": "WOMEN",
                "price": 140.00,
                "discount_price": 99.00,
                "stock": 20,
                "is_featured": True,
                "description": "Flowy floral printed Mulberry silk midi wrap dress with v-neck and tie waist.",
                "short_description": "Elegant silk midi wrap dress.",
                "rating": 4.9,
                "num_reviews": 50,
                "image_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Women's High-Waisted Tailored Trousers",
                "category": cat_trousers,
                "brand": brand_urban,
                "gender": "WOMEN",
                "price": 85.00,
                "discount_price": 65.00,
                "stock": 35,
                "is_featured": True,
                "description": "Chic high-waisted pleated wide-leg trousers for modern office style.",
                "short_description": "High-waisted pleated wide-leg trousers.",
                "rating": 4.8,
                "num_reviews": 31,
                "image_url": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Women's Leather Ankle Boots",
                "category": cat_shoes,
                "brand": brand_sole,
                "gender": "WOMEN",
                "price": 175.00,
                "discount_price": 139.00,
                "stock": 18,
                "is_featured": True,
                "description": "Sleek pointed-toe leather ankle boots with block heel.",
                "short_description": "Pointed-toe leather block heel boots.",
                "rating": 4.7,
                "num_reviews": 24,
                "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&auto=format&fit=crop&q=80"
            },
            {
                "name": "Women's Linen Casual Button-Down Shirt",
                "category": cat_shirts,
                "brand": brand_urban,
                "gender": "WOMEN",
                "price": 70.00,
                "discount_price": 54.99,
                "stock": 40,
                "is_featured": False,
                "description": "Breathable 100% French linen relaxed fit blouse shirt.",
                "short_description": "Relaxed fit 100% French linen blouse shirt.",
                "rating": 4.6,
                "num_reviews": 16,
                "image_url": "https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=800&auto=format&fit=crop&q=80"
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

        self.stdout.write(self.style.SUCCESS("Clothing & Footwear seed data successfully created!"))

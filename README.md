# Modern Full-Stack E-Commerce Store Template

A complete, production-ready **E-Commerce Store Platform** featuring a **Django REST Framework (DRF)** backend and a **Next.js 15 (React 19 + Tailwind CSS v4)** frontend.

---

## Key Features

### Backend (Django REST Framework)
1. **Core Package (`store_core`)**: Refactored settings, URLs, WSGI, and Celery configuration.
2. **User & Authentication (`users`)**: Custom `User` model, `UserProfile`, and `ShippingAddress` model with Token & OTP Auth.
3. **Products Catalog (`products`)**: `Category`, `Brand`, `Product`, `ProductImage`, and `Review` models with search, filter, and ordering endpoints.
4. **Shopping Cart (`cart`)**: Guest and user `Cart` & `CartItem` management endpoints (`add_item`, `update_item`, `remove_item`, `clear`).
5. **Orders & Checkout (`orders`)**: `Order` & `OrderItem` models, status workflows (`PENDING`, `PROCESSING`, `SHIPPED`, `DELIVERED`), and summary calculations.
6. **Payments Integration (`payments`)**: Stripe Checkout & PaymentIntent endpoints.
7. **Swagger OpenAPI Documentation**: Auto-generated interactive API docs at `/api-docs/`.

### Frontend (Next.js 15 + React 19 + Tailwind CSS v4)
1. **Glassmorphism Design**: Responsive UI with dark-mode aesthetic, gradient accents, and micro-animations.
2. **Global State Context (`CartContext`)**: Instant cart count badge updates, persistent guest carts, and seamless DRF API synchronization.
3. **Interactive Navigation & Header**: Search bar with instant query redirect, cart side drawer toggle, user profile dropdown.
4. **Homepage**: Hero banner, Category Grid, Featured Products, Special Offers, and Customer Testimonials.
5. **Products Catalog**: Category filtering, price sorting, search filtering, and responsive grid layout.
6. **Product Detail View**: Gallery preview, stock status, quantity picker, and customer reviews.
7. **Shopping Cart Page**: Item quantity manager, subtotal/tax/shipping breakdown, and checkout redirect.
8. **Checkout Flow**: Shipping address form, payment selector, and order confirmation dialog.
9. **Order History**: User order tracking page.

---

## How to Run the Project

### Running Backend (Django)

```bash
# 1. Install Dependencies
pip install -r requirements.txt

# 2. Run Database Migrations
python manage.py makemigrations products cart orders payments users
python manage.py migrate

# 3. Seed Initial E-Commerce Products & Categories
python manage.py seed_ecommerce

# 4. Start Development Server
python manage.py runserver 0.0.0.0:8000
```

### Running Frontend (Next.js)

```bash
cd frontend

# 1. Install NPM Dependencies
npm install

# 2. Start Development Server
npm run dev

# 3. Build Production Bundle
npm run build
```

---

## API Endpoints

- `GET /api/products/` - List products with search (`?search=`), category filter (`?category__slug=`), ordering.
- `GET /api/categories/` - List active categories.
- `GET /api/cart/` - Retrieve current shopping cart.
- `POST /api/cart/add_item/` - Add item to cart.
- `POST /api/orders/create_order/` - Submit new customer order.
- `POST /api/payments/create-intent/` - Initialize Stripe payment intent.
- `GET /api-docs/` - Interactive Swagger API documentation.

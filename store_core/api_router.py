from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from users.api.views import (
    UserViewSet,
    SignupViewSet,
    LoginViewSet,
    verifyOtpView,
    sendOtpView,
    resetEmailView,
    resetPasswordView,
    userProfileView,
    deleteUserView,
    AdminUserViewSet,
    ShippingAddressViewSet
)
from products.views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet
)
from cart.views import CartViewSet
from orders.views import OrderViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# Auth & User Routes
router.register("users", UserViewSet, basename="users")
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("verify-otp", verifyOtpView, basename="verify-otp")
router.register("send-otp", sendOtpView, basename="send-otp")
router.register("reset-email", resetEmailView, basename="reset-email")
router.register("reset-password", resetPasswordView, basename="reset-password")
router.register("user-profile", userProfileView, basename="user-profile")
router.register("addresses", ShippingAddressViewSet, basename="addresses")
router.register("delete-user", deleteUserView, basename="delete-user")
router.register("admin_users", AdminUserViewSet, basename="admin-users")

# E-Commerce Routes
router.register("categories", CategoryViewSet, basename="categories")
router.register("brands", BrandViewSet, basename="brands")
router.register("products", ProductViewSet, basename="products")
router.register("cart", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename="orders")

app_name = "api"
urlpatterns = router.urls

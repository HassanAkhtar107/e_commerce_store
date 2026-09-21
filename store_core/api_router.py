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
    SubscriptionPlanViewSet,
    UserSubscriptionViewSet,
    UserPaymentMethodViewSet
)

from templates.api.views import (
    TemplatesView,
    FieldsView,
    GeneratedDocumentViewSet,
    CompanyViewSet,
    CompanyFieldsViewSet,
    TemplateChapterViewSet,
    CategoryViewSet,
    FixedFieldsByAdminViewSet
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("verify-otp", verifyOtpView, basename="verify-otp")
router.register("send-otp", sendOtpView, basename="send-otp")
router.register("reset-email", resetEmailView, basename="reset-email")
router.register("reset-password", resetPasswordView, basename="reset-password")
router.register("user-profile", userProfileView, basename="user-profile")
router.register("delete-user", deleteUserView, basename="delete-user")
router.register("admin_users", AdminUserViewSet, basename="admin-users")

# subscriptions
router.register("subscription-plans", SubscriptionPlanViewSet, basename="subscription-plans")
router.register("user-subscriptions", UserSubscriptionViewSet, basename="user-subscriptions")
router.register("payment-methods", UserPaymentMethodViewSet, basename="payment-methods")
# templates
router.register("templates", TemplatesView, basename="template")
router.register("fields", FieldsView, basename="field")
router.register("generated-documents", GeneratedDocumentViewSet, basename="generated-document")
router.register("company", CompanyViewSet, basename="companies")
router.register("company-fields", CompanyFieldsViewSet, basename="company-fields")
router.register("chapters", TemplateChapterViewSet, basename="chapter")
router.register("categories", CategoryViewSet, basename="category")
router.register("fixed-fields-by-admin", FixedFieldsByAdminViewSet, basename="fixed-fields-by-admin")


app_name = "api"
urlpatterns = router.urls

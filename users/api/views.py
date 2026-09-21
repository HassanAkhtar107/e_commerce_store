import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet, ViewSet
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from users.models import User, UserProfile, SubscriptionPlan, UserSubscription, UserPaymentMethod
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    UserPaymentMethodSerializer,
    SignupSerializer,
    AdminUserSerializer
)
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import TokenAuthentication
from .response_messages import *
from ..helpers import *

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SignupViewSet(ModelViewSet):
    """
    # Request
    {
        "username":"email",
        "password":"password"
    }
    # 200 Response{
        "token": <auth_token>,
        "user" : user_details,
    }
    """

    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data["id"])
        user_serializer = UserSerializer(user,context={"request":request})
        token, created = Token.objects.get_or_create(user=user)
        data = {"token": token.key, "user": user_serializer.data}
        return Response(data=data, status=status.HTTP_200_OK)

class LoginViewSet(ViewSet):
    """
    # Request
    {
        "username":"email",
        "password":"password"
    }
    # 200 Response if user not verified{
        "status":"ERROR",
        "token": <auth_token>,
        "user" : user_details,
        "message": "otp sended"
    }
    # 200 Response if user verified{
        "token": <auth_token>,
        "user" : user_details
    }
    """
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        if user.is_verified == True:
            # Allow ADMIN users to always log in
            # For regular users, check for active subscription
            if user.user_type != "ADMIN":
                has_active_sub = user.subscriptions.filter(status="active").exists()
                if not has_active_sub:
                    return Response(
                        {"non_field_errors": ["Your account does not have an active subscription. Please contact the administrator."]},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            return Response(
                {"token": token.key, "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )

        sendOtpEmail(user)
        data = {
            "token": token.key,
            "user": user_serializer.data,
        }

        return Response(data=data, status=status.HTTP_200_OK)

        
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class verifyOtpView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def list(self,request):
        otp = self.request.GET.get("otp", None)
        if otp is None:
            data = {"status": "ERROR", "message": "otp is required for verification"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        verify = verifyOtp(user, otp)
        if verify == True:
            token = Token.objects.get(user=user)
            data = {"status": "OK", "token": token.key, "message": "email verified"}
            return Response(data=data, status=status.HTTP_200_OK)

        data = {"status": "ERROR", "message": "Invalid OTP"}
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class sendOtpView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def list(self,request):
        user = self.request.user
        sendOtpEmail(user)
        data = {"status": "OK", "message": "OTP is sended to registered email"}
        return Response(data=data, status=status.HTTP_200_OK)


class resetEmailView(ViewSet):
    
    def list(self,request):
        email = self.request.GET.get("email", None)
        if email is None:
            data = {"status": "ERROR", "message": "email is required"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(email=email)
        except:
            data = {"status": "ERROR", "message": "invalid email address"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        sendOtpEmail(user)
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "status": "OK",
            "token": token.key,
            "message": "OTP is sended to registered email",
            "user_type":user.user_type
        }
        return Response(data=data, status=status.HTTP_200_OK)



class resetPasswordView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def create(self,request):
        
        password1 = request.data.get("password1", None)
        password2 = request.data.get("password2", None)

        if password1 is None or password2 is None:
            data = {"status": "ERROR", "message": "password1 and password2 is required"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        if password1 != password2:
            data = {
                "status": "ERROR",
                "message": "password1 and password2 should be same",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if len(password1) < 8:
            data = {
                "status": "ERROR",
                "message": "password should be minimum of 8 characters.",
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.set_password(password1)
        user.save()

        data = {"status": "OK", "message": "Password Reset Successfullly!"}
        return Response(data=data, status=status.HTTP_200_OK)



class userProfileView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class: UserProfileSerializer
    queryset= UserProfile.objects.all()
    http_method_names = ['get','update','delete']
    
    def list(self,request):
        instance = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    def update(self,request):
        try:
            instance = UserProfile.objects.get(user=request.user)
            serializer = self.serializer_class(instance, data=request.data)
        except:
            serializer = self.serializer_class(data=request.data)
            
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request):
        instance = UserProfile.objects.get(user=request.user)
        instance.delete()
        data = {"status": "ok", "message": delete_response}
        return Response(data=data, status=status.HTTP_200_OK)


class deleteUserView(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def list(self,request):
        user = request.user
        user.delete()
        data = {"status": "OK", "message": delete_response}
        return Response(data=data, status=status.HTTP_200_OK)


from rest_framework.permissions import BasePermission

class IsAdminUserType(BasePermission):
    """
    Allows access only to users with user_type == 'ADMIN'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "ADMIN")


class AdminUserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserType]
    authentication_classes = [TokenAuthentication]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all().order_by('-id')

    def get_queryset(self):
        # Exclude superusers if we only want to manage regular app users, 
        # or just return all users. Let's return all users for now.
        return super().get_queryset()


import stripe
from django.conf import settings

class SubscriptionPlanViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SubscriptionPlanSerializer
    queryset = SubscriptionPlan.objects.all()

    def create(self, request, *args, **kwargs):
        if request.user.user_type != "ADMIN":
            return Response({"error": "Only admins can create plans"}, status=status.HTTP_403_FORBIDDEN)
        
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        
        name = request.data.get('name')
        price = request.data.get('price')
        description = request.data.get('description', '')

        if not name or not price:
            return Response({"error": "Name and price are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create product in Stripe
            product = stripe.Product.create(name=name, description=description)
            # Create price in Stripe (Assuming USD and recurring monthly for simplicity, adjust as needed)
            stripe_price = stripe.Price.create(
                unit_amount=int(float(price) * 100), # cents
                currency="usd",
                recurring={"interval": "month"},
                product=product.id,
            )

            plan = SubscriptionPlan.objects.create(
                name=name,
                price=price,
                description=description,
                stripe_product_id=product.id,
                stripe_price_id=stripe_price.id
            )
            serializer = self.get_serializer(plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e), "traceback": traceback.format_exc()}, status=status.HTTP_400_BAD_REQUEST)

class UserSubscriptionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()
    
    @action(detail=False, methods=['get'])
    def my_subscription(self, request):
        try:
            sub = UserSubscription.objects.get(user=request.user)
            serializer = self.get_serializer(sub)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserSubscription.DoesNotExist:
            return Response({"message": "No active subscription"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def assign_subscription(self, request):
        if request.user.user_type != "ADMIN":
            return Response({"error": "Only admins can assign subscriptions"}, status=status.HTTP_403_FORBIDDEN)

        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')

        user_id = request.data.get('user_id')
        plan_id = request.data.get('plan_id')

        if not user_id or not plan_id:
            return Response({"error": "user_id and plan_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=user_id)
            plan = SubscriptionPlan.objects.get(id=plan_id)

            # Verify user has a Stripe customer ID and a payment method
            if not target_user.stripe_customer_id:
                return Response({"error": "User does not have a Stripe customer. Please add a payment method first."}, status=status.HTTP_400_BAD_REQUEST)

            if not target_user.payment_methods.exists():
                return Response({"error": "User does not have a payment method. Please add one first."}, status=status.HTTP_400_BAD_REQUEST)

            if not plan.stripe_price_id:
                return Response({"error": "This plan does not have a Stripe price ID."}, status=status.HTTP_400_BAD_REQUEST)

            # Cancel existing Stripe subscription if any
            user_sub, created = UserSubscription.objects.get_or_create(user=target_user)
            if user_sub.stripe_subscription_id:
                try:
                    stripe.Subscription.cancel(user_sub.stripe_subscription_id)
                except Exception:
                    pass  # Old subscription may already be cancelled

            # Create a real Stripe subscription — this will charge the default payment method on the customer
            stripe_sub = stripe.Subscription.create(
                customer=target_user.stripe_customer_id,
                items=[{"price": plan.stripe_price_id}],
                # We rely on the customer's default_payment_method set in Stripe
                payment_behavior="error_if_incomplete",
            )

            # Save locally
            user_sub.plan = plan
            user_sub.stripe_subscription_id = stripe_sub.id
            user_sub.status = stripe_sub.status  # e.g. 'active', 'incomplete'
            user_sub.save()

            return Response({"message": "Subscription assigned and payment initiated successfully", "stripe_status": stripe_sub.status}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserPaymentMethodViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = UserPaymentMethodSerializer

    def get_queryset(self):
        queryset = UserPaymentMethod.objects.all()
        user_id = self.request.query_params.get("user")
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        elif self.request.user.user_type != "ADMIN":
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @action(detail=False, methods=['post'])
    def create_setup_intent(self, request):
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            target_user = User.objects.get(id=user_id)
            
            # Helper to find or create a Stripe customer (always searches by email to avoid duplicates)
            def _get_or_create_stripe_customer(user):
                # If user already has a stripe_customer_id, verify it's still valid
                if user.stripe_customer_id:
                    try:
                        customer = stripe.Customer.retrieve(user.stripe_customer_id)
                        if not customer.get('deleted', False):
                            return customer
                    except stripe.error.InvalidRequestError:
                        pass  # Customer doesn't exist anymore, fall through
                
                # Search Stripe for an existing customer with this email
                existing = stripe.Customer.list(email=user.email, limit=1)
                if existing.data:
                    customer = existing.data[0]
                    user.stripe_customer_id = customer.id
                    user.save(update_fields=['stripe_customer_id'])
                    return customer
                
                # No existing customer found — create a new one
                customer = stripe.Customer.create(
                    email=user.email,
                    name=user.name,
                    metadata={'user_id': user.id}
                )
                user.stripe_customer_id = customer.id
                user.save(update_fields=['stripe_customer_id'])
                return customer
            
            # Always ensure we have a valid Stripe customer
            _get_or_create_stripe_customer(target_user)
            
            # Create SetupIntent — handle deleted/invalid Stripe customers
            try:
                intent = stripe.SetupIntent.create(
                    customer=target_user.stripe_customer_id,
                    payment_method_types=["card"],
                )
            except stripe.error.InvalidRequestError as e:
                # Customer was deleted from Stripe — find or recreate and clean up stale data
                UserPaymentMethod.objects.filter(user=target_user).delete()
                _get_or_create_stripe_customer(target_user)
                intent = stripe.SetupIntent.create(
                    customer=target_user.stripe_customer_id,
                    payment_method_types=["card"],
                )
            
            return Response({
                'client_secret': intent.client_secret
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        user_id = request.data.get('user')
        pm_id = request.data.get('stripe_payment_method_id')
        card_name = request.data.get('card_name', '')

        if not user_id or not pm_id:
            return Response({"error": "user and stripe_payment_method_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=user_id)
            
            # Verify stored Stripe customer ID if present
            if target_user.stripe_customer_id:
                try:
                    cust = stripe.Customer.retrieve(target_user.stripe_customer_id)
                    if not cust.get('deleted', False):
                        # Customer exists and is valid – use it
                        pass
                except stripe.error.InvalidRequestError:
                    # Stored ID invalid, will find/create below
                    target_user.stripe_customer_id = None
                        
            # Ensure we have a valid Stripe customer before attaching payment method
            def _get_or_create_customer(user):
                # Search by email first
                existing = stripe.Customer.list(email=user.email, limit=5)
                if existing.data:
                    cust = existing.data[0]
                    user.stripe_customer_id = cust.id
                    user.save(update_fields=['stripe_customer_id'])
                    return cust
                # Create new customer
                cust = stripe.Customer.create(
                    email=user.email,
                    name=user.name,
                    metadata={'user_id': user.id}
                )
                user.stripe_customer_id = cust.id
                user.save(update_fields=['stripe_customer_id'])
                return cust

            _get_or_create_customer(target_user)
            
            # 2. Attach Payment Method to Customer (handle already attached case)
            try:
                stripe.PaymentMethod.attach(pm_id, customer=target_user.stripe_customer_id)
            except stripe.error.InvalidRequestError as e:
                # If the payment method is already attached to this customer, ignore the error
                if getattr(e, 'code', None) == 'payment_method_already_attached':
                    pass
                else:
                    raise
            
            # 3. Save metadata locally
            pm_details = stripe.PaymentMethod.retrieve(pm_id)
            card = pm_details.get('card', {})
            
            # Create local record
            # Check if this is the first payment method for the user
            is_first = not UserPaymentMethod.objects.filter(user=target_user).exists()
            
            user_pm = UserPaymentMethod.objects.create(
                user=target_user,
                stripe_payment_method_id=pm_id,
                card_name=card_name,
                last4=card.get('last4'),
                brand=card.get('brand'),
                exp_month=str(card.get('exp_month')),
                exp_year=str(card.get('exp_year')),
                is_active=is_first
            )

            # If it's the first card, also set it as default in Stripe automatically
            if is_first:
                try:
                    stripe.Customer.modify(
                        target_user.stripe_customer_id,
                        invoice_settings={'default_payment_method': pm_id}
                    )
                except:
                    pass
            
            serializer = self.get_serializer(user_pm)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def set_default(self, request):
        """Set a given payment method as the default for the user's Stripe customer."""
        user_id = request.data.get('user')
        pm_id = request.data.get('stripe_payment_method_id')
        if not user_id or not pm_id:
            return Response({"error": "user and stripe_payment_method_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            payment_method = UserPaymentMethod.objects.get(user=target_user, stripe_payment_method_id=pm_id)
        except UserPaymentMethod.DoesNotExist:
            return Response({"error": "Payment method not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        
        # Ensure Stripe customer exists
        if not target_user.stripe_customer_id:
             # Search by email first
            existing = stripe.Customer.list(email=target_user.email, limit=1)
            if existing.data:
                target_user.stripe_customer_id = existing.data[0].id
                target_user.save(update_fields=['stripe_customer_id'])
            else:
                cust = stripe.Customer.create(
                    email=target_user.email,
                    name=target_user.name,
                    metadata={'user_id': target_user.id}
                )
                target_user.stripe_customer_id = cust.id
                target_user.save(update_fields=['stripe_customer_id'])

        # Set as default in Stripe
        try:
            stripe.Customer.modify(
                target_user.stripe_customer_id,
                invoice_settings={'default_payment_method': pm_id}
            )
            # Update local state
            UserPaymentMethod.objects.filter(user=target_user).update(is_active=False)
            payment_method.is_active = True
            payment_method.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = self.get_serializer(payment_method)
        return Response(serializer.data, status=status.HTTP_200_OK)

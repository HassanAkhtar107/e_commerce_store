import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from orders.models import Order

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")


class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        order_number = request.data.get("order_number")
        if not order_number:
            return Response({"error": "order_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_number=order_number)
            amount_cents = int(order.total_amount * 100)

            if stripe.api_key:
                intent = stripe.PaymentIntent.create(
                    amount=amount_cents,
                    currency="usd",
                    metadata={"order_number": order.order_number},
                )
                order.stripe_payment_intent_id = intent.id
                order.save()

                return Response({
                    "clientSecret": intent.client_secret,
                    "order_number": order.order_number,
                    "amount": order.total_amount
                }, status=status.HTTP_200_OK)
            else:
                # Return demo checkout response if stripe key is not set
                order.payment_status = "PAID"
                order.order_status = "PROCESSING"
                order.save()
                return Response({
                    "message": "Demo Payment Processed Successfully (Stripe Key Pending)",
                    "order_number": order.order_number,
                    "amount": order.total_amount,
                    "status": "PAID"
                }, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

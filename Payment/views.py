from django.db import transaction

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema

from Core.base_viewsets import BaseModelViewSet

from .models import Payment
from .serializer import PaymentSerializer

from Discount.models import DiscountUsage


@extend_schema(
    tags=['Payments'],
    summary='Payments',
    description='Manage user payments.'
)
class PaymentViewSet(BaseModelViewSet):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Payment.objects.filter(
            order__user=self.request.user
        )

    @extend_schema(
        summary='Pay Order',
        description='Simulate a successful payment for the selected order.',
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "payment_id": {"type": "integer"},
                    "order_id": {"type": "integer"},
                    "payment_status": {"type": "string"},
                    "order_status": {"type": "string"},
                }
            }
        }
    )
    @action(
        detail=True,
        methods=['post']
    )
    @transaction.atomic
    def pay(self, request, pk=None):

        payment = self.get_object()

        # جلوگیری از پرداخت دوباره

        if payment.status == 'success':

            return Response(
                {
                    'message': 'Payment already completed.',
                    'payment_id': payment.id,
                    'order_id': payment.order.id,
                    'payment_status': payment.status,
                    'order_status': payment.order.status,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order = payment.order

        # فقط سفارش Pending قابل پرداخت است

        if order.status != 'pending':

            return Response(
                {
                    'message': 'Only pending orders can be paid.',
                    'order_id': order.id,
                    'order_status': order.status,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ===========================================
        # Payment Success
        # ===========================================

        payment.status = 'success'

        payment.save(
            update_fields=['status']
        )

        # ===========================================
        # Update Order Status
        # ===========================================

        order.status = 'paid'

        order.save(
            update_fields=['status']
        )

        # ===========================================
        # Register Discount Usage
        # ===========================================

        if order.discount:

            DiscountUsage.objects.get_or_create(
                discount=order.discount,
                user=order.user,
                order=order
            )

        # ===========================================
        # Response
        # ===========================================

        return Response(
            {
                'message': 'Payment successful',
                'payment_id': payment.id,
                'order_id': order.id,
                'payment_status': payment.status,
                'order_status': order.status,
            },
            status=status.HTTP_200_OK
        )
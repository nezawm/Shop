
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from Core.base_viewsets import BaseModelViewSet
from .models import Order, OrderItem
from .serializer import OrderSerializer, CheckoutSerializer
from Payment.models import Payment
from Discount.models import Discount, DiscountUsage
from Products.models import ProductVariant


# ===========================================
# Order CRUD
# ===========================================

@extend_schema(tags=["Orders"])
class OrderViewSet(BaseModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    @extend_schema(
        tags=["Orders"],
        summary="Cancel Order",
        description="Cancel a pending order and restore product stock.",
        request=None,
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="cancel"
    )
    @transaction.atomic
    def cancel(self, request, pk=None):

        order = get_object_or_404(
            Order,
            id=pk,
            user=request.user
        )

        if order.status == "cancelled":
            return Response(
                {
                    "message": "Order already cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status != "pending":
            return Response(
                {
                    "message": "Only pending orders can be cancelled."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in order.items.select_related("variant"):
            ProductVariant.all_objects.filter(
                id=item.variant.id
            ).update(
                stock=F("stock") + item.quantity
            )

        order.status = "cancelled"

        order.save(
            update_fields=["status"]
        )

        payment = Payment.objects.filter(
            order=order
        ).first()

        if payment:
            payment.status = "failed"

            payment.save(
                update_fields=["status"]
            )

        return Response(
            {
                "message": "Order cancelled successfully.",
                "order_id": order.id,
                "status": order.status,
            },
            status=status.HTTP_200_OK
        )
# ===========================================
# Checkout
# ===========================================
@extend_schema(
    tags=["Orders"],
    summary="Checkout",
    description="Create a new order from cart and create pending payment.",
    request=CheckoutSerializer
)
class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        serializer = CheckoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            cart = request.user.cart

        except Exception:

            return Response(
                {
                    "error": "Cart does not exist."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cart.items.exists():

            return Response(
                {
                    "error": "Cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.select_related(
            "variant",
            "variant__product"
        )

        for item in cart_items:

            if not item.variant.is_active:
                return Response(
                    {
                        "error": f"{item.variant.product.name} is not available."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if item.quantity > item.variant.stock:
                return Response(
                    {
                        "error": (
                            f"Insufficient stock for "
                            f"{item.variant.product.name}. "
                            f"Available stock: {item.variant.stock}, "
                            f"Requested: {item.quantity}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        discount_code = serializer.validated_data.get(
            "discount_code"
        )

        discount = None

        original_price = cart.total_price

        final_price = original_price

        # ===========================================
        # Discount validation
        # ===========================================

        if discount_code:

            try:

                discount = Discount.objects.get(
                    code=discount_code
                )

            except Discount.DoesNotExist:

                return Response(
                    {
                        "error": "Invalid discount code."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # بررسی فعال بودن کد تخفیف

            if not discount.is_active:

                return Response(
                    {
                        "error": "Discount code is inactive."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # بررسی تاریخ انقضا

            if (
                discount.expired_at
                and discount.expired_at <= timezone.now()
            ):

                return Response(
                    {
                        "error": "Discount code has expired."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ===========================================
            # بررسی استفاده قبلی از کد تخفیف
            # ===========================================

            already_used = DiscountUsage.objects.filter(
                discount=discount,
                user=request.user
            ).exists()

            if already_used:

                return Response(
                    {
                        "error": (
                            "You have already used "
                            "this discount code."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ===========================================
            # بررسی اولین خرید
            # ===========================================

            if discount.is_first_purchase:

                has_previous_purchase = Order.objects.filter(
                    user=request.user,
                    status__in=[
                        "paid",
                        "processing",
                        "shipped",
                        "delivered",
                    ]
                ).exists()

                if has_previous_purchase:

                    return Response(
                        {
                            "error": (
                                "This discount is only available "
                                "for your first purchase."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # ===========================================
            # محاسبه تخفیف
            # ===========================================

            discount_amount = (
                original_price * discount.percentage
            ) / 100

            final_price = (
                original_price - discount_amount
            )

        # ===========================================
        # Create Order
        # ===========================================

        order = Order.objects.create(
            user=request.user,
            total_price=final_price,
            discount=discount,
            discount_amount=(
                original_price - final_price
                if discount
                else 0
            ),
            status="pending"
        )
        order_items = []

        # ===========================================
        # بررسی موجودی و کم کردن Stock
        # ===========================================

        for item in cart_items:

            updated = ProductVariant.objects.filter(
                id=item.variant.id,
                stock__gte=item.quantity
            ).update(
                stock=F("stock") - item.quantity
            )

            if updated == 0:

                return Response(
                    {
                        "error": (
                            f"{item.variant.product.name} "
                            "stock is insufficient."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            order_items.append(

                OrderItem(
                    order=order,
                    variant=item.variant,
                    quantity=item.quantity,
                    price=item.variant.price
                )

            )

        # ===========================================
        # Create Order Items
        # ===========================================

        OrderItem.objects.bulk_create(
            order_items
        )

        # ===========================================
        # Create Payment
        # ===========================================

        payment = Payment.objects.create(
            order=order,
            amount=final_price,
            status="pending"
        )

        # ===========================================
        # Empty Cart
        # ===========================================

        cart.items.all().delete()

        return Response(
            {
                "message": "Order created successfully.",

                "order_id": order.id,

                "payment_id": payment.id,

                "original_price": original_price,

                "discount_code": (
                    discount.code
                    if discount
                    else None
                ),

                "discount_percentage": (
                    discount.percentage
                    if discount
                    else 0
                ),

                "final_price": final_price,

                "payment_status": payment.status,
            },
            status=status.HTTP_201_CREATED
        )
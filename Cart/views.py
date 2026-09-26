from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from Core.base_viewsets import BaseModelViewSet
from Cart.models import Cart, CartItem
from Cart.serializer import CartSerializer, CartItemSerializer
from django.conf import settings


@extend_schema(tags=['Cart'])
class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


@extend_schema(tags=['Cart'])
class CartItemViewSet(BaseModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )

    def perform_create(self, serializer):

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        variant = serializer.validated_data['variant']
        quantity = serializer.validated_data['quantity']

        if (
                not CartItem.objects.filter(cart=cart, variant=variant).exists()
                and
                cart.items.count() >= settings.MAX_CART_ITEMS
        ):
            raise ValidationError(
                {
                    "message": f"You can only have {settings.MAX_CART_ITEMS} different products in your cart."
                }
            )

        cart_item = CartItem.objects.filter(
            cart=cart,
            variant=variant
        ).first()

        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            serializer.save(cart=cart)

from rest_framework import serializers

from Core.base_serializer import BaseSerializer
from .models import Order, OrderItem




class OrderItemSerializer(BaseSerializer):

    product_name = serializers.CharField(
        source='variant.product.name',
        read_only=True
    )

    size = serializers.CharField(
        source='variant.size.size',
        read_only=True
    )

    color = serializers.CharField(
        source='variant.color.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'variant',
            'product_name',
            'size',
            'color',
            'quantity',
            'price',
        ]

class OrderSerializer(BaseSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'total_price',
            'items',
            'created_at',
        ]
######################################################################### Checkout



class CheckoutSerializer(serializers.Serializer):
    discount_code = serializers.CharField(
        required=False,
        allow_blank=True
    )
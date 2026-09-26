from rest_framework import serializers

from Core.base_serializer import BaseSerializer
from .models import Cart, CartItem

class CartItemSerializer(BaseSerializer):
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

    unit_price = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'variant',
            'product_name',
            'size',
            'color',
            'quantity',
            'unit_price',
            'total_price',
        ]


class CartSerializer(BaseSerializer):

    items = CartItemSerializer(many=True, read_only=True)

    total_items = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'items',
            'total_items',
            'total_price',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
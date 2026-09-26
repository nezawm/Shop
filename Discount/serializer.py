from rest_framework import serializers

from Core.base_serializer import BaseSerializer
from .models import Discount


class DiscountSerializer(BaseSerializer):

    class Meta:
        model = Discount
        fields = [
            'id',
            'code',
            'percentage',
            'is_active',
            'created_at',
            'expired_at',
        ]
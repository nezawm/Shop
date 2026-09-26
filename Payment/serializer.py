
from rest_framework import serializers

from Core.base_serializer import BaseSerializer
from .models import Payment


class PaymentSerializer(BaseSerializer):

    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'amount',
            'status',
            'created_at',
        ]
        read_only_fields = [
            'order',
            'amount',
            'status',
            'created_at'
        ]
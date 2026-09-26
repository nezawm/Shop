from rest_framework import serializers
from rest_framework import serializers
from Order.models import Order

from Accounts.models import CustomUser


class DailySalesSerializer(serializers.Serializer):
    date = serializers.DateField()
    orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

class MonthlySalesSerializer(serializers.Serializer):
    month = serializers.CharField()
    orders = serializers.IntegerField()
    total_sales = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

class OrdersCountSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    paid_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    cancelled_orders = serializers.IntegerField()

class TopProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    total_sold = serializers.IntegerField()


class TopCustomerSerializer(serializers.Serializer):
        user = serializers.SerializerMethodField()

        class Meta:
            model = CustomUser
            fields = [
                'user',
                'orders',
                'total_spent'
            ]

        def get_user(self, obj):
            full_name = f"{obj.first_name} {obj.last_name}".strip()

            return full_name if full_name else obj.phone_number


class LowStockSerializer(serializers.Serializer):
    product = serializers.CharField()
    size = serializers.CharField()
    color = serializers.CharField()
    stock = serializers.IntegerField()




class CancelledOrderSerializer(serializers.ModelSerializer):

    order_id = serializers.IntegerField(source='id')
    customer = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'order_id',
            'customer',
            'total_price',
            'created_at',
        )

    def get_customer(self, obj):

        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()

        return full_name or obj.user.phone_number

class PaymentReportSerializer(serializers.Serializer):

    successful_payments = serializers.IntegerField()

    failed_payments = serializers.IntegerField()

    pending_payments = serializers.IntegerField()

    successful_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    failed_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
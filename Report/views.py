from django.shortcuts import render

# Create your views here.


from django.utils import timezone
from drf_spectacular.utils import extend_schema
from django.db.models import Count, Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Value
from django.db.models.functions import Concat
from Accounts.models import CustomUser
from Order.models import Order, OrderItem
from Report.serializers import DailySalesSerializer, MonthlySalesSerializer, OrdersCountSerializer, TopProductSerializer, \
    TopCustomerSerializer, LowStockSerializer, CancelledOrderSerializer, PaymentReportSerializer
from Products.models import ProductVariant
from django.db.models import Sum
from Payment.models import Payment
#####################################
#daily   1
#monthly 2
#order-count 3
#top-product 4
#top-customer 5
#low-stock(5) 6
#cancelled-order 7
#payment-report 8
#####################################

@extend_schema(
    tags=['Reports'],
    summary='Daily Sales Report',
    description='Returns total paid orders and total sales for today.'
)
class DailySalesReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        today = timezone.now().date()

        orders = Order.objects.filter(
            created_at__date=today,
            status='paid'
        )

        total_sales = orders.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        data = {
            'date': today,
            'orders': orders.count(),
            'total_sales': total_sales,
        }

        serializer = DailySalesSerializer(data)

        return Response(serializer.data)

@extend_schema(
    tags=['Reports'],
    summary='Monthly Sales Report',
    description='Returns total paid orders and total sales for the current month.'
)
class MonthlySalesReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        today = timezone.now()

        orders = Order.objects.filter(
            created_at__year=today.year,
            created_at__month=today.month,
            status='paid'
        )

        total_sales = orders.aggregate(
            total=Sum('total_price')
        )['total'] or 0

        data = {
            'month': today.strftime('%Y-%m'),
            'orders': orders.count(),
            'total_sales': total_sales,
        }

        serializer = MonthlySalesSerializer(data)

        return Response(serializer.data)


@extend_schema(
    tags=['Reports'],
    summary='Orders Count Report',
    description='Returns statistics of all orders grouped by status.'
)
class OrdersCountReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        data = {
            'total_orders': Order.objects.count(),
            'paid_orders': Order.objects.filter(status='paid').count(),
            'pending_orders': Order.objects.filter(status='pending').count(),
            'cancelled_orders': Order.objects.filter(status='cancelled').count(),
        }

        serializer = OrdersCountSerializer(data)

        return Response(serializer.data)


@extend_schema(
    tags=['Reports'],
    summary='Top Selling Products',
    description='Returns products ordered by total quantity sold.'
)
class TopProductsReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        products = (
            OrderItem.objects
            .filter(order__status='paid')
            .values('variant__product__name')#دسته بندی بر اساس محصول
            .annotate(total_sold=Sum('quantity'))#مجموع تعداد فروش هر مخصول
            .order_by('-total_sold')#از بیشترین به کمترین فروش
        )

        data = [
            {
                'product_name': item['variant__product__name'],
                'total_sold': item['total_sold']
            }
            for item in products
        ]

        serializer = TopProductSerializer(data, many=True)

        return Response(serializer.data)


@extend_schema(
    tags=['Reports'],
    summary='Top Customers',
    description='Returns customers ordered by total purchase amount.'
)

class TopCustomersReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        customers = (
            CustomUser.objects
            .annotate(
                orders=Count(
                    'orders',
                    filter=Q(orders__status='paid')
                ),
                total_spent=Sum(
                    'orders__total_price',
                    filter=Q(orders__status='paid')
                )
            )
            .filter(total_spent__isnull=False)
            .order_by('-total_spent')
        )

        serializer = TopCustomerSerializer(
            customers,
            many=True
        )

        return Response(serializer.data)

@extend_schema(
    tags=['Reports'],
    summary='Low Stock Report',
    description='Returns product variants with stock less than 5.'
)
class LowStockReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        variants = ProductVariant.objects.filter(
            stock__lt=5
        ).order_by('stock')

        data = []

        for variant in variants:

            data.append({
                'product': variant.product.name,
                'size': str(variant.size),
                'color': variant.color.name,
                'stock': variant.stock,
            })

        serializer = LowStockSerializer(
            data,
            many=True
        )

        return Response(serializer.data)



@extend_schema(
    tags=['Reports'],
    summary='Cancelled Orders Report',
    description='Returns all cancelled orders.'
)
class CancelledOrdersReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        orders = (
            Order.objects
            .filter(status='cancelled')
            .select_related('user')
            .annotate(
                customer=Concat(
                    'user__first_name',
                    Value(' '),
                    'user__last_name'
                )
            )
            .order_by('-created_at')
        )

        serializer = CancelledOrderSerializer(
            orders,
            many=True
        )

        return Response(serializer.data)

@extend_schema(
    tags=['Reports'],
    summary='Payments Report',
    description='Returns statistics of successful, failed and pending payments.'
)
class PaymentReportView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        successful = Payment.objects.filter(
            status='success'
        )

        failed = Payment.objects.filter(
            status='failed'
        )

        pending = Payment.objects.filter(
            status='pending'
        )

        data = {

            'successful_payments': successful.count(),

            'failed_payments': failed.count(),

            'pending_payments': pending.count(),

            'successful_amount':
                successful.aggregate(
                    total=Sum('amount')
                )['total'] or 0,

            'failed_amount':
                failed.aggregate(
                    total=Sum('amount')
                )['total'] or 0,

        }

        serializer = PaymentReportSerializer(data)

        return Response(serializer.data)
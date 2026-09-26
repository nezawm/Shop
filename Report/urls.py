from django.urls import path

from Report.views import DailySalesReportView, MonthlySalesReportView, OrdersCountReportView, TopProductsReportView, \
    TopCustomersReportView, LowStockReportView, CancelledOrdersReportView, PaymentReportView

urlpatterns=[
    path('daily-sales/',DailySalesReportView.as_view(),name='daily-sales'),
    path('monthly-sales/',MonthlySalesReportView.as_view(),name='monthly-sales'),
    path('orders-count/',OrdersCountReportView.as_view(),name='orders-count'),
    path('top-products/',TopProductsReportView.as_view(),name='top-products'),
    path('top-customers/',TopCustomersReportView.as_view(),name='top-customers'),
    path('low-stock/',LowStockReportView.as_view(),name='low-stock'),
    path('cancelled-orders/',CancelledOrdersReportView.as_view(),name='cancelled-orders'),
    path('payment-report',PaymentReportView.as_view(),name='payment-report'),

]
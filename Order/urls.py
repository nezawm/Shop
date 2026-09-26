from django.urls import path, include
from rest_framework import routers

from .views import OrderViewSet, CheckoutView

router = routers.DefaultRouter()

router.register(
    'order',
    OrderViewSet,
    basename='order'
)

urlpatterns = [

    path(
        '',
        include(router.urls)
    ),

    path(
        'checkout/',
        CheckoutView.as_view(),
        name='checkout'
    ),

]
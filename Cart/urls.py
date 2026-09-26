from django.urls import path, include
from rest_framework import routers

from Cart.views import CartViewSet, CartItemViewSet

urlpatterns=[

]

router=routers.DefaultRouter()

router.register('cart',CartViewSet,basename='Cart')
router.register('cart_item',CartItemViewSet,basename='cart_item')

urlpatterns+=[
    path('',include(router.urls)),
]
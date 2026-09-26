
from django.urls import path, include
from rest_framework import routers

from Products.views import CategoryViewSet, ProductSizeViewSet, BrandViewSet, ProductViewSet, ProductImageViewSet, \
    ColorViewSet, ProductVariantViewSet

urlpatterns=[]


router = routers.DefaultRouter()

router.register('category', CategoryViewSet, basename='category'),
router.register('size',ProductSizeViewSet,basename='size'),
router.register('brand',BrandViewSet,basename='brand'),
router.register('product',ProductViewSet,basename='product'),
router.register('image',ProductImageViewSet,basename='image'),
router.register('color',ColorViewSet,basename='color'),
router.register('variant',ProductVariantViewSet,basename='variant'),

urlpatterns+=[
    path('',include(router.urls)),
]


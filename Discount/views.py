from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from Core.base_viewsets import BaseModelViewSet
from .models import Discount
from .serializer import DiscountSerializer


@extend_schema(
    tags=['Discounts'],
    summary='Discount Codes',
    description='Manage discount codes that can be applied during checkout.'
)
class DiscountViewSet(BaseModelViewSet):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    queryset = Discount.objects.all()
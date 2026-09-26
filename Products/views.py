
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.parsers import MultiPartParser, FormParser
from Core.base_viewsets import BaseModelViewSet
from Products.models import Category, ProductSize, Brand, Product, ProductImage, Color, ProductVariant
from Products.serializer import CategorySerializer, ProductSizeSerializer, BrandSerializer, ProductSerializer, \
    ProductImageSerializer, ColorSerializer,ProductVariantSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from Products.filters import ProductFilter, ProductVariantFilter, ColorFilter, ProductSizeFilter, BrandFilter, \
    CategoryFilter


# Create your views here.
@extend_schema(tags=['Products'])
class CategoryViewSet(BaseModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filterset_class = CategoryFilter

    search_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]
@extend_schema(tags=['Products'])
class ProductSizeViewSet(BaseModelViewSet):
    serializer_class = ProductSizeSerializer
    queryset = ProductSize.objects.all()
    search_fields = [
        "size",
    ]
    filterset_class = ProductSizeFilter

    ordering_fields = [
        "size",
        "created_at",
    ]

    ordering = [
        "size",
    ]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

@extend_schema(tags=['Products'])
class BrandViewSet(BaseModelViewSet):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    search_fields = [
        "name",
        "description",
    ]
    filterset_class = BrandFilter

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

@extend_schema(tags=['Products'])
class ProductViewSet(BaseModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_class = ProductFilter

    search_fields = [
        "name",
        "brand__name",
        "category__name",
        "description",
    ]

    ordering_fields = [
        "created_at",
        "name",
    ]
    ordering = [
        "-created_at",
    ]

    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
    ]

@extend_schema(tags=['Products'])
class ProductImageViewSet(BaseModelViewSet):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
    ]

    @extend_schema(exclude=True)
    def list(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

@extend_schema(tags=['Products'])
class ColorViewSet(BaseModelViewSet):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    filterset_class = ColorFilter

    search_fields = [
        "name",
        "color_code",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]

    ordering = [
        "name",
    ]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

@extend_schema(tags=['Products'])
class ProductVariantViewSet(BaseModelViewSet):
    serializer_class = ProductVariantSerializer
    queryset = ProductVariant.objects.all()
    filterset_class = ProductVariantFilter

    search_fields = [
        "product__name",
        "color__name",
        "size__size",
    ]

    ordering_fields = [
        "price",
        "stock",
    ]

    ordering = [
        "price",
    ]

    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]
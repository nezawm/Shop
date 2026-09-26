from rest_framework import serializers

from Core.base_serializer import BaseSerializer
from Products.models import Category, Brand, Product, Color, ProductImage, ProductVariant, ProductSize
from rest_framework import serializers
from .models import ProductVariant



class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields=['id','name','is_active','created_at','updated_at']


class BrandSerializer(BaseSerializer):
    class Meta:
        model = Brand
        fields=['id','name','description','created_at','logo']

class ProductSizeSerializer(BaseSerializer):
    class Meta:
        model = ProductSize
        fields=['id','size','created_at','updated_at']

class ColorSerializer(BaseSerializer):
    class Meta:
        model = Color
        fields=['id','color_code','name','created_at']

class ProductImageSerializer(BaseSerializer):
    class Meta:
        model = ProductImage
        fields=['id','product','image','created_at','updated_at']



class ProductVariantSerializer(BaseSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    size_name = serializers.CharField(
        source='size.size',
        read_only=True
    )

    color_name = serializers.CharField(
        source='color.name',
        read_only=True
    )

    class Meta:
        model = ProductVariant
        fields = [
            'id',

            'product',
            'product_name',

            'image',

            'size',
            'size_name',

            'color',
            'color_name',

            'price',
            'stock',
            'discount',
        ]


class ProductSerializer(BaseSerializer):
    category=CategorySerializer(read_only=True)
    brand=BrandSerializer(read_only=True)
    image=ProductImageSerializer(read_only=True,many=True)
    variant=ProductVariantSerializer(read_only=True,many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'brand',
            'image',
            'variant',
            'created_at',
            'updated_at',
        ]
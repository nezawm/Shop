from django.contrib import admin

from Core.base_admin import SoftDeleteAdmin
from .models import *


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(SoftDeleteAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(ProductSize)
class ProductSizeAdmin(SoftDeleteAdmin):
    list_display = ('id', 'size', 'created_at')


@admin.register(Brand)
class BrandAdmin(SoftDeleteAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(SoftDeleteAdmin):
    list_display = ('id', 'name', 'color_code')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(SoftDeleteAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'brand',
        'is_active',
        'created_at',
    )

    list_filter = (
        'category',
        'brand',
        'is_active',
    )

    search_fields = (
        'name',
        'description',
        'brand__name',
        'category__name',
    )

    autocomplete_fields = (
        'category',
        'brand',
    )

    inlines = (
        ProductImageInline,
        ProductVariantInline,
    )


@admin.register(ProductImage)
class ProductImageAdmin(SoftDeleteAdmin):
    list_display = (
        'id',
        'product',
        'created_at',
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(SoftDeleteAdmin):
    list_display = (
        'id',
        'product',
        'size',
        'color',
        'price',
        'stock',
        'discount',
    )

    list_filter = (
        'size',
        'color',
    )

    search_fields = (
        'product__name',
    )
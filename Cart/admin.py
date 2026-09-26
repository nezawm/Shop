from django.contrib import admin

# Register your models here.
from django.contrib import admin

from Core.base_admin import SoftDeleteAdmin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(SoftDeleteAdmin):

    list_display = (
        'id',
        'user',
        'total_items',
        'total_price',
        'created_at',
        'updated_at',
        'deleted',
    )

    list_filter = (
        'is_deleted',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__phone_number',
    )


@admin.register(CartItem)
class CartItemAdmin(SoftDeleteAdmin):

    list_display = (
        'id',
        'cart',
        'variant',
        'quantity',
        'unit_price',
        'total_price',
        'created_at',
        'deleted',
    )

    list_filter = (
        'is_deleted',
        'created_at',
    )

    search_fields = (
        'cart__user__username',
        'cart__user__phone_number',
        'variant__product__name',
    )
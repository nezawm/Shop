from django.contrib import admin

# Register your models here.
from django.contrib import admin

from Core.base_admin import SoftDeleteAdmin
from .models import Discount


@admin.register(Discount)
class DiscountAdmin(SoftDeleteAdmin):

    list_display = (
        'id',
        'code',
        'percentage',
        'is_active',
        'created_at',
        'expired_at',
    )

    list_filter = (
        'is_active',
        'created_at',
        'expired_at',
    )

    search_fields = (
        'code',
    )

    readonly_fields = (
        'created_at',
    )
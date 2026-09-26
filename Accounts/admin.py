# accounts/admin.py
from django.contrib import admin

from Core.base_admin import SoftDeleteAdmin
from .models import Address, Profile, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'first_name', 'last_name', 'gender', 'phone_number', 'birth_date', 'created_at', 'updated_at', 'is_active')

    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')

    list_filter = ('gender', 'is_active', 'created_at', 'updated_at')


@admin.register(Address)
class AddressAdmin(SoftDeleteAdmin):

    list_display = ('id', 'user', 'city', 'street', 'postal_code')

    list_filter = ('user', 'city')

    search_fields = ('city', 'street', 'user__username', 'user__phone_number')

@admin.register(Profile)
class ProfileAdmin(SoftDeleteAdmin):

    list_display = ('id', 'user', 'phone_number', 'is_verified', 'created_at', 'updated_at')

    list_filter = ('is_verified', 'created_at', 'updated_at')

    search_fields = ('user__username', 'phone_number')

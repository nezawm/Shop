from django.contrib.auth import get_user_model
from rest_framework import serializers

from Accounts.models import Address, Profile, CustomUser
from Core.base_serializer import BaseSerializer

user=get_user_model()



class AddressSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields=[
            'id',
            'city',
            'street',
            'postal_code',
        ]

class ProfileSerializer(BaseSerializer):
    class Meta:
        model = Profile
        fields=[
            'id',
            'avatar',
            'phone_number',
            'is_verified',
            'created_at',
            'updated_at',
        ]



class CustomUserSerializer(BaseSerializer):
    addresses = AddressSerializer(many=True,read_only=True)
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields=[
            'id',
            'username',
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'birth_date',
            'is_active',
            'is_staff',
            'is_superuser',
            'created_at',
            'updated_at',
            'addresses',
            'profile',
        ]

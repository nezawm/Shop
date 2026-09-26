from drf_spectacular.utils import extend_schema

from Core.base_viewsets import BaseModelViewSet
from Accounts.models import CustomUser, Address, Profile
from Accounts.serializer import (
    CustomUserSerializer,
    AddressSerializer,
    ProfileSerializer,
)


@extend_schema(
    tags=['Accounts'],
    summary='Users',
    description='Manage application users.'
)
class CustomUserViewSet(BaseModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


@extend_schema(
    tags=['Accounts'],
    summary='Addresses',
    description='Manage user addresses.'
)
class AddressViewSet(BaseModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()


@extend_schema(
    tags=['Accounts'],
    summary='Profiles',
    description='Manage user profiles.'
)
class ProfileViewSet(BaseModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
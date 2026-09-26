from django.urls import include, path
from rest_framework import routers

from Accounts.views import CustomUserViewSet, AddressViewSet, ProfileViewSet

urlpatterns=[

]

router = routers.DefaultRouter()

router.register('customuser',CustomUserViewSet,basename='CustomUser')
router.register('address',AddressViewSet,basename='Address')
router.register('profile',ProfileViewSet,basename='Profile')

urlpatterns+=[
    path('',include(router.urls)),
]
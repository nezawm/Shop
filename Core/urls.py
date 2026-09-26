from django.urls import path, include
from rest_framework import routers

from Core.views import OtpVerifyView, OtpCreateView

urlpatterns = [
    path('otp/create',OtpCreateView.as_view(),name='otp_create'),
    path('otp/verify',OtpVerifyView.as_view(),name='otp_verify'),


    # path('', home, name='home'),
]




router=routers.DefaultRouter()


urlpatterns+=[
    path('',include(router.urls)),
]
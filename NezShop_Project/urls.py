"""
URL configuration for NezShop_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from NezShop_Project import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Core.urls')),
    path('accounts/',include('Accounts.urls')),
    path('products/',include('Products.urls')),
    path('cart/',include('Cart.urls')),
    path('order/',include('Order.urls')),
    path('discounts/',include('Discount.urls')),
    path('payments/', include('Payment.urls')),
    path('reports/',include('Report.urls')),
    path ('',include('rest_framework.urls')),
]

urlpatterns += [
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),

    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain'),
    path('api/token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

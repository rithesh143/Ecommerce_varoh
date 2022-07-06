"""ecommerce_ravi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views
from shop.views import google_index

admin.site.site_header = 'Varoh Games Admin'
# admin.site.index_title = 'Varoh Games'
admin.site.site_title = 'Varoh Games'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('orders/', include('orders.urls')),
    path('auth/', include('users.urls')),
    path('api-token-auth/', token_views.obtain_auth_token),
    path('googleff4301433a1854f8', google_index),
    path('googleff4301433a1854f8.html', google_index),
]

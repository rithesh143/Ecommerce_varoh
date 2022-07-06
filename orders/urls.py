from django.urls import path
from . import views

urlpatterns = [
    path('create', views.CreateOrder.as_view()),
    path('copun', views.GetCopun.as_view()),
    path('checkout/test', views.TestCheckout.as_view()),
    path('verify', views.VerifyOrder.as_view()),
    path('list', views.OrdersList.as_view()),
    path('csv_report', views.orders_csv, name='orders_csv'),
]
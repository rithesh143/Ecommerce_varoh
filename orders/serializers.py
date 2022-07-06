from rest_framework import serializers
from .models import Order, OrderItem, Copun

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['name', 'category', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

class CopunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Copun
        fields = '__all__'
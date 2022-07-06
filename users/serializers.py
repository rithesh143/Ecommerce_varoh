from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'phone', 'full_name', 'pin_code', 'house', 'area', 'landmark', 'town', 'state']


class UserSerializer(serializers.ModelSerializer):
    address_list = AddressSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'address_list']

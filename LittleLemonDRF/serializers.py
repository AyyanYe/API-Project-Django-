# serializers.py
from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'price': {'min_value': 2},
        }

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'price': {'min_value': 2},
            'unit_price': {'min_value': 0.1},
            'quantity': {'min_value': 1},  # Changed to minimum 1 for valid quantity
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'total': {'min_value': 0},
        }

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'price': {'min_value': 2},
            'unit_price': {'min_value': 0.1},
            'quantity': {'min_value': 1},  # Changed to minimum 1 for valid quantity
        }

from rest_framework import serializers
from .models import User, Restaurant, Dish, Order, OrderItem, Review, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'email', 'phone', 'address', 'role', 'image', 'level', 'coin', 'created_at', 'updated_at']
        extra_kwargs = {
            'role': {'default': "user"},
            'image': {'required': False},
            'level': {'required': False, 'default': 1},
            'coin': {'required': False, 'default': 0},
        }

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'opening_hours', 'created_at', 'updated_at']

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'img', 'price', 'rate', 'type', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'quantity', 'options', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Đưa vào dữ liệu các món trong đơn hàng
    class Meta:
        model = Order
        fields = ['id', 'user', 'restaurant', 'order_date', 'price', 'ship', 'discount', 'total_amount', 'created_at', 'updated_at', 'order_items']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'item', 'user', 'rating', 'comment', 'created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'quantity', 'created_at', 'updated_at']

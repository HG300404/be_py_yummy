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
        fields = ['id', 'name', 'phone', 'address', 'opening_hours', 'user_id', 'created_at', 'updated_at']

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'restaurant_id', 'name', 'img', 'price', 'rate', 'type', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'item_id', 'quantity', 'options', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
  #  order_items = OrderItemSerializer(many=True, read_only=True)  # Đưa vào dữ liệu các món trong đơn hàng
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'restaurant_id', 'price', 'ship', 'discount', 'total_amount', 'payment', 'created_at', 'updated_at']
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'order_id','restaurant_id', 'user_id', 'rating', 'comment', 'created_at', 'updated_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'item_id', 'restaurant_id', 'quantity', 'created_at', 'updated_at']

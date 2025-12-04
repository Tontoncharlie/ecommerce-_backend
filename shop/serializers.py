from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = user.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user 
    
class ProductSerializer(serializers.ModelSerializer):
    class meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class meta:
        model = Order
        fields = ('id', 'user', 'created_at', 'total_price', 'items')
        read_only_fields = ('user', 'created_at', 'total_price', 'items')



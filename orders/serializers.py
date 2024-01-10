from rest_framework import serializers
from orders.models import Order, OrderItem
from rest_framework import serializers
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(source='name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user_account = serializers.ReadOnlyField(source='user_account.user.username')
    products = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_account', 'products', 'total_price', 'created_at', 'updated_at', 'is_completed']
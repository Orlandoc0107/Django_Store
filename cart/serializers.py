from rest_framework import serializers
from cart.models import Cart, CartProduct
from products.serializers import ProductSerializer


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):

    cartproduct_set = CartProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_account', 'created_at', 'updated_at', 'ordered', 'paid', 'cartproduct_set']

        read_only_fields = ['user_account', 'created_at', 'updated_at', 'ordered', 'paid', ]


# En tu serializer


class CartSerializer(serializers.ModelSerializer):
    cartproduct_set = CartProductSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user_account', 'created_at', 'updated_at', 'ordered', 'paid', 'cartproduct_set', 'total_price']

        read_only_fields = ['user_account', 'created_at', 'updated_at', 'ordered', 'paid', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'quantity', 'price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['total_price'] = instance.quantity * instance.price
        return representation

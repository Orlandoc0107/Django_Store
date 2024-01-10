from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from cart.models import Cart
from django.contrib.auth.models import User



class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class OrderListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user_account=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user_account=request.user)

        order = Order.objects.create(user_account=request.user, total_price=cart.total_price)

        for cart_product in cart.cartproduct_set.all():
            OrderItem.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)

        cart.cartproduct_set.all().delete()
        cart.update_totals()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
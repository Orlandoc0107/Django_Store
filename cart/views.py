from rest_framework import viewsets, status, permissions
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from products.models import Product
from cart.models import Cart, CartProduct
from cart.serializers import CartSerializer, CartProductSerializer
from django.shortcuts import get_object_or_404


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CartDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user_account=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CartProductCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user_account=request.user)
        product_data = request.data.get('product')

        if not product_data or 'id' not in product_data:
            return Response({'detail': 'Product ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_data['id'], is_available=True)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found or not available.'}, status=status.HTTP_404_NOT_FOUND)

        quantity = product_data.get('quantity', 1)

        if quantity <= 0:
            return Response({'detail': 'Invalid quantity.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity > product.quantity:
            return Response({'detail': 'Not enough quantity available.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_product = cart.cartproduct_set.filter(product=product).first()
        if existing_product:
            return Response({'detail': 'Product already in the cart.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_product = CartProduct.objects.create(cart=cart, product=product, quantity=quantity,
                                                  price=product.price * quantity)
        cart.update_totals()

        return Response(CartProductSerializer(cart_product).data, status=status.HTTP_201_CREATED)

# {
#   "product": {
#     "id": 1,
#     "quantity": 2
#   }
# }


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CartProductUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user_account=request.user)
        product_id = kwargs.get('product_id')

        if not product_id:
            return Response({'detail': 'Product ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found or not available.'}, status=status.HTTP_404_NOT_FOUND)

        existing_product = cart.cartproduct_set.filter(product=product).first()
        if not existing_product:
            return Response({'detail': 'Product not in the cart.'}, status=status.HTTP_400_BAD_REQUEST)

        quantity_to_update = request.data.get('quantity', 1)

        if quantity_to_update <= 0:
            return Response({'detail': 'Invalid quantity to update.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_update > product.quantity:
            return Response({'detail': 'Not enough quantity available.'}, status=status.HTTP_400_BAD_REQUEST)

        existing_product.quantity = quantity_to_update
        existing_product.price = product.price * quantity_to_update
        existing_product.save()

        cart.update_totals()

        return Response({'detail': 'Product quantity updated successfully.'}, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CartProductDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user_account=request.user)
        product_id = kwargs.get('product_id')

        if not product_id:
            return Response({'detail': 'Product ID not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found or not available.'}, status=status.HTTP_404_NOT_FOUND)

        existing_product = cart.cartproduct_set.filter(product=product).first()
        if not existing_product:
            return Response({'detail': 'Product not in the cart.'}, status=status.HTTP_400_BAD_REQUEST)

        quantity_to_remove = request.data.get('quantity', 1)

        if quantity_to_remove <= 0:
            return Response({'detail': 'Invalid quantity to remove.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_remove > existing_product.quantity:
            return Response({'detail': 'Invalid quantity to remove.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity_to_remove == existing_product.quantity:
            existing_product.delete()
        else:
            existing_product.quantity -= quantity_to_remove
            existing_product.save()

        cart.update_totals()

        return Response({'detail': 'Product removed or quantity reduced successfully.'},
                        status=status.HTTP_200_OK)


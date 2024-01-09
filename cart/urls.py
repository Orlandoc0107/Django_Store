from django.urls import path
from rest_framework import routers
from cart import views
from cart.views import CartDetailAPIView, CartProductCreateAPIView, CartProductUpdateAPIView, CartProductDeleteAPIView

router = routers.DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')


urlpatterns = [
    path('cart/', CartDetailAPIView.as_view()),
    path('cart/product/create/', CartProductCreateAPIView.as_view()),
    path('cart/product/update/<int:product_id>/', CartProductUpdateAPIView.as_view()),
    path('cart/product/delete/<int:pk>/', CartProductDeleteAPIView.as_view()),
]

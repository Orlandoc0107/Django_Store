from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView, OrderItemDetailAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view()),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view()),
    path('order-items/<int:pk>/', OrderItemDetailAPIView.as_view()),
]
from django.urls import path
from rest_framework import routers
from products import views
from products.views import ProductListCreateView, ProductPOSTView, ProductDetailView, ProductPUTView
from products.views import ProductDELETEView, ImageListCreateView


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('products/create/', ProductPOSTView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),
    path('products/edit/<int:pk>/', ProductPUTView.as_view()),
    path('products/<int:pk>/delete/', ProductDELETEView.as_view()),
    path('products/<int:product_id>/images/', ImageListCreateView.as_view()),
]

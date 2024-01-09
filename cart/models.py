from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user_account = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    total_quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_totals(self):
        self.total_quantity = sum(item.quantity for item in self.cartproduct_set.all())
        self.total_price = sum(item.get_subtotal() for item in self.cartproduct_set.all())
        self.save()

    def add_product(self, product, quantity=1, price=None):
        cart_product, created = CartProduct.objects.get_or_create(cart=self, product=product, defaults={'quantity': quantity, 'price': price})
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        self.update_totals()

    def remove_product(self, product):
        try:
            cart_product = self.cartproduct_set.get(product=product)
            cart_product.delete()
            self.update_totals()
        except CartProduct.DoesNotExist:
            pass



class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_subtotal(self):
        return self.quantity * self.price

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=False)
    on_sale = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    images = models.ManyToManyField('Photo', related_name='product_images')

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Photo {self.id}"

from rest_framework import serializers
from products.models import Product, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def create(self, validated_data):

        product_id = self.context.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        photo = Photo.objects.create(**validated_data)

        product.images.add(photo)
        return photo


class ProductSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'created_at', 'updated_at', 'code',
                  'is_available', 'on_sale', 'brand', 'model', 'origin', 'category', 'images', ]

        read_only_fields = ['id', 'description', 'created_at', 'updated_at', 'code',
                            'brand', 'model', 'origin', 'category', 'images', ]


class ProductSerializerPUT(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'created_at', 'updated_at', 'code',
                  'is_available', 'on_sale', 'brand', 'model', 'origin', 'category', 'images', ]

        read_only_fields = ['id', 'created_at', 'updated_at', 'images', ]

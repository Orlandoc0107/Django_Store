# Generated by Django 5.0.1 on 2024-01-10 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_rename_stock_product_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
    ]

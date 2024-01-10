from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Accounts
from cart.models import Cart
from orders.models import Order
from orders.models import OrderItem


User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser and perform additional setup'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting setup...'))

        username = 'admin'
        email = 'admin@admin.com'
        password = 'admin'

        existing_user = User.objects.filter(username=username).first()

        if not existing_user:
            superuser = User.objects.create_superuser(username, email, password)

            account = Accounts.objects.create(user=superuser)

            cart = Cart.objects.create(user_account=superuser)

            order = Order.objects.create(user_account=superuser, total_price=0, is_completed=False)

            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))

        self.stdout.write(self.style.SUCCESS('Setup completed successfully.'))
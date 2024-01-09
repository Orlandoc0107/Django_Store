from django.db import models
from django.contrib.auth.models import User


class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    dni = models.CharField(max_length=255, null=True, blank=True, unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    website = models.URLField()
    phone = models.CharField(max_length=255, null=True, blank=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)


    def verify_security_answer(self, user_answer):
        return self.answer == user_answer
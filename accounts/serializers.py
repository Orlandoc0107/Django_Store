from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Accounts


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']


class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ['id', 'age', 'dni', 'address', 'city',
                  'state_province', 'country', 'website',
                  'phone', 'avatar']

        read_only_fields = ['id', 'avatar']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['avatar']


class SecurityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ('question', 'answer')


class SecuritySerializer(serializers.ModelSerializer):
    answer = serializers.CharField(write_only=True)

    class Meta:
        model = Accounts
        fields = ('answer',)


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField()


    def validate_new_password(self, value):
        return value


class UsernameChangeSerializer(serializers.Serializer):
    new_username = serializers.CharField(max_length=150)


    def validate_new_username(self, value):

        return value

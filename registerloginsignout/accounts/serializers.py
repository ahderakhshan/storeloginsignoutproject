from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Userloginsignout


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSignoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userloginsignout
        fields = ('user', 'login_date', 'signout_date')
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


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserLoginSignoutSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    login_length=serializers.SerializerMethodField('get_login_length')
    class Meta:
        model = Userloginsignout
        fields = ('user', 'login_date', 'signout_date', 'login_length')

    def get_login_length(self, userloginsignout):
        length = userloginsignout.signout_date-userloginsignout.login_date
        total_seconds = length.total_seconds()
        hour = int(total_seconds/3600)
        minute = int((total_seconds-hour*3600)/60)
        second = total_seconds-(hour*3600)-(minute*60)
        return (hour,minute,second)
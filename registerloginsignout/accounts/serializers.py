from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Userloginsignout
from jalali_date import datetime2jalali


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
    login_length = serializers.SerializerMethodField('get_login_length')
    jalali_signout_date = serializers.SerializerMethodField('get_jalali_signout_date')
    jalali_login_date = serializers.SerializerMethodField('get_jalali_login_date')

    class Meta:
        model = Userloginsignout
        fields = ('user', 'login_date', 'signout_date', 'login_length', 'jalali_signout_date', 'jalali_login_date')

    def get_login_length(self, userloginsignout):
        try:
            length = userloginsignout.signout_date-userloginsignout.login_date
            total_seconds = length.total_seconds()
            hour = int(total_seconds/3600)
            minute = int((total_seconds-hour*3600)/60)
            second = total_seconds-(hour*3600)-(minute*60)
            return (hour,minute,second)
        except:
            return (-1 , -1 , -1)

    def get_jalali_signout_date(self, userloginsignout):
        try:
            return datetime2jalali(userloginsignout.signout_date).strftime("%y/%m/%d %H:%M:%S")
        except:
            return "not signout yet"

    def get_jalali_login_date(self, userloginsignout):
        try:
            return (datetime2jalali(userloginsignout.login_date)).strftime("%y/%m/%d %H:%M:%S")
        except:
            return "not login yet"

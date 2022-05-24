from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Userloginsignout
import datetime


class CreateUser(APIView):
    permission_classes = [IsAdminUser, ]

    def post(self, request):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        request.user.auth_token.delete()
        uls = Userloginsignout.objects.filter(user=request.user).last()
        uls.signout_date = datetime.datetime.now()
        uls.save()
        return Response(
            data={'message': 'logout successful'},
            status=status.HTTP_204_NO_CONTENT
        )

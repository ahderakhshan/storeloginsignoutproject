from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSignoutSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Userloginsignout, User
from rest_framework.exceptions import ValidationError
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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000


class AllActivities(generics.ListAPIView):
    queryset = Userloginsignout.objects.all()
    serializer_class = UserLoginSignoutSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = StandardResultsSetPagination


class UserActivity(generics.ListAPIView):
    queryset = Userloginsignout.objects.all()
    serializer_class = UserLoginSignoutSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            username = self.request.query_params['username']
        except:
            raise ValidationError(detail="no query parameter")
        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationError(detail="no user with this username")
        return Userloginsignout.objects.filter(user=user)


class UserActivityInDate(generics.ListAPIView):
    queryset = Userloginsignout.objects.all()
    serializer_class = UserLoginSignoutSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        try:
            username = self.request.query_params['username']
        except:
            raise ValidationError(detail="no username in query parameter")
        try:
            year = self.request.query_params['year']
            month = self.request.query_params['month']
            day = self.request.query_params['day']
        except:
            raise ValidationError(detail="no date in query parameter")
        try:
            user = User.objects.get(username=username)
        except:
            raise ValidationError(detail="no user with this username")
        return Userloginsignout.objects.filter(user=user, login_date__year=year, login_date__month=month
                                               , login_date__day=day)

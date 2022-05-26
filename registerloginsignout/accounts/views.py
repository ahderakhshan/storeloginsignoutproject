import jdatetime
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSignoutSerializer
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .models import Userloginsignout, User
from rest_framework.exceptions import ValidationError
import datetime
import pytz


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
        tz = pytz.timezone('Asia/Tehran')
        if not request.user.is_superuser:
            request.user.auth_token.delete()
            uls = Userloginsignout.objects.filter(user=request.user).last()
            uls.signout_date = datetime.datetime.now(tz)
            uls.save()
            return Response(
                data={'message': 'logout successful'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            request.user.auth_token.delete()
            return Response(
                data={'message': 'logout successful'},
                status=status.HTTP_204_NO_CONTENT
            )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 10000


class AllActivities(generics.ListAPIView):
    queryset = Userloginsignout.objects.filter(user__is_superuser=False).order_by('-login_date')
    serializer_class = UserLoginSignoutSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = StandardResultsSetPagination


class UserActivity(generics.ListAPIView):
    queryset = Userloginsignout.objects.all().order_by('-login_date')
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
        return Userloginsignout.objects.filter(user=user).order_by('-login_date')


class UserActivityInDate(generics.ListAPIView):
    queryset = Userloginsignout.objects.all().order_by('-login_date')
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
                                               , login_date__day=day).order_by('-login_date')


class AdvanceSearchUsersActivities(generics.ListAPIView):
    queryset = Userloginsignout.objects.filter(user__is_superuser=False).order_by('-login_date')
    serializer_class = UserLoginSignoutSerializer
    permission_classes = [AllowAny, ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {'user__username': ['contains', 'exact'], 'login_date': ['gte', ]
        , 'signout_date': ['lte', ]}

    def list(self, request, *args, **kwargs):
        objs = super().list(request, *args, **kwargs)
        return objs


class JalaliSearch(APIView):
    def get(self, request):
        try:
            login = request.query_params['login_date']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        date_login = jdatetime.datetime.strptime(login, '%y-%m-%d').date()
        date_login = jdatetime.date.togregorian(date_login)
        try:
            username = request.query_params['username']
        except:
            username = None
        try:
            user = User.objects.get(username=username)
        except:
            if username is not None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if username is None:
            ser_result = UserLoginSignoutSerializer(Userloginsignout.objects.filter(login_date__year=date_login.year,
                                                                                login_date__month=date_login.month,
                                                                                login_date__day=date_login.day)
                                                                                , many=True)
        else:
            ser_result = UserLoginSignoutSerializer(Userloginsignout.objects.filter(login_date__year=date_login.year,
                                                                                    login_date__month=date_login.month,
                                                                                    login_date__day=date_login.day,
                                                                                    user=user)
                                                    , many=True)
        return Response(ser_result.data, status=status.HTTP_200_OK)

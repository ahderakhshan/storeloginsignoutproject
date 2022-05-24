from django.urls import path
#from rest_framework.authtoken import views as tokenviews
from .views import CreateUser
from .authentication import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token),
    path('signup/', CreateUser.as_view()),
]

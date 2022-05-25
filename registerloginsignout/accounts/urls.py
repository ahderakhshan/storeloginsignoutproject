from django.urls import path
#from rest_framework.authtoken import views as tokenviews
from .views import CreateUser, UserLogout, AllActivities, UserActivity, UserActivityInDate, AdvanceSearchUsersActivities
from .authentication import obtain_auth_token
from .authentication2 import obtain_auth_token2


urlpatterns = [
    path('login/', obtain_auth_token),
    path('signup/', CreateUser.as_view()),
    path('logout/', UserLogout.as_view()),
    path('allactivities/', AllActivities.as_view()),
    path('useractivity/', UserActivity.as_view()),
    path('useractivityindate/', UserActivityInDate.as_view()),
    path('advancesearch/', AdvanceSearchUsersActivities.as_view()),
    path('loginmanager/', obtain_auth_token2)
]

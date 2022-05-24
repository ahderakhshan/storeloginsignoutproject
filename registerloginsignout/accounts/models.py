from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Userloginsignout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(auto_now_add=True)
    signout_date = models.DateTimeField(null=True)


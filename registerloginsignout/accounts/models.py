from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Userloginsignout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateTimeField(null=True)
    signout_date = models.DateTimeField(null=True)

    def __str__(self):
        return "user:" + self.user.username + "| login:" + str(self.login_date) + "| logout:" + str(self.signout_date)

from django.db import models

class UserInfo(models.Model):
    userName = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    mobilePhone = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


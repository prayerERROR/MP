from django.db import models


class UserInfo(models.Model):
    user_name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    mobile_phone = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

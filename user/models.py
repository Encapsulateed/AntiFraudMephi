from django.db import models
from django.db.models import Model


class User(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    money = models.FloatField(max_length=15, default=0)


class Transaction(models.Model):
    money = models.FloatField(max_length=15, default=0.0)
    user_from = models.IntegerField(default=0)
    user_to = models.IntegerField(default=0)
    screen_resolution = models.CharField(max_length=20, default=0)
    color_depth = models.IntegerField(default=0)
    id_35_38 = models.CharField(max_length=200, default='')
    device_type = models.CharField(max_length=100, default='')
    card_type_1 = models.CharField(max_length=100, default='')
    card_type_2 = models.CharField(max_length=100, default='')
    c1_c14 = models.CharField(max_length=500, default='')
    d1_d15 = models.CharField(max_length=500, default='')
    m1_m3 = models.CharField(max_length=100, default='')
    m5_m9 = models.CharField(max_length=100, default='')
    v1_v339 = models.CharField(max_length=5000, default='')
    os = models.CharField(max_length=100, default='')
    brouser = models.CharField(max_length = 100, default='')

    # Здесь должно быть гораздо больше полей

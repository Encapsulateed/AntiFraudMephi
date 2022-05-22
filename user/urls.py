from django.contrib import admin
from django.urls import path, include
from user.views import *

urlpatterns = [
    path('', showMain),
    path('autorise/', autorise),
    path('registration/', registration,name="registration"),
    path('about/', about),
    path('autorise/account/',login,name="account"),
    path('autorise/account/transactions/',go_to_transactions),
    path('autorise/account/addmoney/',add_money)
]

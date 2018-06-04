from django.db import models

from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User


# class User_details(User):
#     name = models.CharField(max_length=100, blank=True, default='')
#     email = models.EmailField(max_length=70,blank=False)
#     # password = models.CharField(max_legnth=250, widget=serializers.PasswordInput)
#     Token = models.CharField(max_length=200,blank=False)

class Payment_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_amount = models.IntegerField(blank=False)
    order_id = models.CharField(max_length=100, blank=False)
    
class Customer(models.Model):
    customer_id = models.CharField(max_length=100, blank=False)

# class Meter_details(models.Model):
#     meter_no = models.IntegerField(blank=False)
#     elec_remain = models.IntegerField(blank=False, default = 0)

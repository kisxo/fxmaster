from django.db import models
import time
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    balance = models.FloatField(default=1000)

def current_unix_time():
    return int(time.time() * 1000)

class Forex(models.Model):
    period = models.PositiveBigIntegerField(default = current_unix_time)
    #open price
    opening = models.FloatField()
    #highest price 
    highest = models.FloatField()
    #lowest price
    lowest = models.FloatField()
    #closing price
    closing = models.FloatField()

class Stock(models.Model):
    period = models.PositiveBigIntegerField(default = current_unix_time)
    price = models.FloatField()

    def __str__(self):
        return f'{self.period}, {self.price}'
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #fixed trade duration in minutes
    duration = models.SmallIntegerField()
    #profit percentage
    profit_margin = models.FloatField()
    side_choice = {
      "UP": "UP",
      "DOWN": "DOWN",
    }
    side = models.CharField(max_length=4, choices=side_choice)
    opening_amount = models.FloatField()
    closing_amount = models.FloatField() 
    status = models.BooleanField(default=False)# update at closing
    
    #calculate values at closing
    result_choice = {
      "Pending": "Pending",
      "Profit": "Profit",
      "Loss": "Loss",
      "Equal": "Equal",
    }
    result = models.CharField(max_length=7, choices=result_choice, default="Pending")#update at closing
    amount_diff = models.FloatField(default=None, null=True)#update at closing
    
    #opening data
    opening_id = models.PositiveIntegerField()
    opening_period = models.PositiveBigIntegerField()
    opening_price = models.FloatField()
    
    #closing data
    closing_id = models.PositiveIntegerField()
    closing_period = models.PositiveBigIntegerField(default = None, null=True)#update at closing
    closing_price = models.FloatField(default = None, null=True)#update at closing
    def __str__(self):
      return f'{self.id}, {self.user_id}'

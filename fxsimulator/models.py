from django.db import models
import time
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    balance = models.FloatField(default=1000)

def current_unix_time():
    return int(time.time() * 1000)

class Stock(models.Model):
    period = models.PositiveBigIntegerField(default = current_unix_time)
    price = models.FloatField()

    def __str__(self):
        return f'{self.period}, {self.price}'
    
class Order(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_duration = models.SmallIntegerField()
    order_side = models.BooleanField()
    order_amount = models.FloatField()
    order_result = models.BooleanField(default=None)
    order_final_amount = models.FloatField(default=None)
    order_diff = models.FloatField(default=None)
    
    start_period_id = models.PositiveIntegerField()
    start_period = models.PositiveBigIntegerField()
    start_period_price = models.FloatField()
    
    end_period_id = models.PositiveIntegerField()
    end_period = models.PositiveBigIntegerField(default = None)
    end_period_price = models.FloatField(default = None)

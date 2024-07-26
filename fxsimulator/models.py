from django.db import models
import time

def current_unix_time():
    return int(time.time() * 1000)

class Stock(models.Model):
    period = models.PositiveBigIntegerField(default = current_unix_time)
    price = models.FloatField()

    def __str__(self):
        return f'{self.period}, {self.price}'

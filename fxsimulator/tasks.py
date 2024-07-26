from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import time 
import math
from fxsimulator.models import Stock

channel_layer = get_channel_layer()
room_id = "fxupdateroom"


@shared_task
def stockSimulator(): 
    try:
        last_stock_price = Stock.objects.all().order_by('-period')[0:1].get().price
    except:
        print("no previous data")
        last_stock_price = 300
    # Example usage
    #S0 = 100  # Initial stock price
    mu = 0.05  # Drift coefficientig 
    sigma = 0.4  # Volatility
    dt = 0.050  # Time step
    # Generate a standard normal random variable using Box-Muller transform
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    
    # Calculate the increment of the Wiener process
    dW = z * math.sqrt(dt)
    
    # Calculate the next stock price
    current_stock_price = last_stock_price * math.exp((mu - 0.5 * sigma**2) * dt + sigma * dW)
    current_period = int(time.time() * 1000)

    print(last_stock_price)
    print(current_stock_price)
    print(current_period)

    Stock(price = current_stock_price, period = current_period).save()
    
    #channel_layer = get_channel_layer()
    #room_id = "fxupdateroom"
    
    async_to_sync(channel_layer.group_send)(
        room_id,
        {
            "type": "fxupdate",
            "data": {
                "period": current_period,
                "price": current_stock_price,
            },
        }
    )
  
    entries = Stock.objects.all()
    results = [[entry.period, entry.price] for entry in entries]

    data = entries
    for row in data:
        print(row)

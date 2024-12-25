from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import time 
import math
from fxsimulator.models import Stock, Forex, Order, User
from django.core.cache import cache

channel_layer = get_channel_layer()
room_id = "fxupdateroom"

def normal_random(mu=0, sigma=1):
    # Box-Muller transform to generate two independent standard normal variables
    u1 = random.random()
    u2 = random.random()
    
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
    
    # Scale and shift to get the desired mean and standard deviation
    return mu + sigma * z0


@shared_task
def priceSimulator():

    S0 = 100  # Initial stock price
    mu = 0.20  # Drift coefficient (annualized)
    sigma = 0.25  # Volatility (annualized)
    T = 1  # Time period in years (1 year simulation)
    dt = 1 / (365 * 24 * 60)  # Time step in years for 1 minute (convert minutes to years)

    # Initialize variables
    try: 
        last_price = cache.get("last_price")
        if last_price is None:
            last_price = S0
    except:
        last_price = S0  # Start with the initial price

    # Simulate GBM for 1 step of 1 minute
    dW = normal_random(0, math.sqrt(dt))  # Brownian motion increment
    new_price = last_price * math.exp((mu - 0.5 * sigma**2) * dt + sigma * dW)  # Update price

    period = int(time.time() * 1000)
    Stock(price = new_price, period = period).save()
    cache.set("last_price", new_price)

    async_to_sync(channel_layer.group_send)(
        room_id,
        {
            "type": "fxupdate",
            "data": {
                "period": period,
                "price": new_price,
            },
        }
    )

@shared_task
def pendingOrderProcessor():
    #order calculation start
    current_stock = Stock.objects.last()

    #orders = Order.objects.filter(closing_id <= current_stock.id)
    orders = Order.objects.filter(closing_id__range=(0, current_stock.id)).filter(status = False)

    print("\nprocessing\n")
    print(current_stock.id)
    print('\n')
    
    # process orders
    for order in orders:
        print('calculating order')
        print(order)

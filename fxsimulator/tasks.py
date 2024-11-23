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
def stockSimulator():
    #price simulation start
    try:
        last_stock_price = Stock.objects.all().order_by('-period')[0:1].get().price
    except:
        print("no previous data")
        last_stock_price = 300
    
    #variables for simulating GBM
    mu = 0.2  # Drift coefficientig 
    sigma = 0.8  # Volatility
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

    #store the new price in database
    Stock(price = current_stock_price, period = current_period).save()
    
    #send a price update to users via channels, ie: websocket
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
    
    #query fresh data from database
    stock_entries = Stock.objects.all()
    #format query data as per highcharts
    stock_data = [[entry.period, entry.price] for entry in stock_entries]
    #store the formated data in cache
    cache.set("stock_data", stock_data, 5)
    cache.set("current_stock", stock_entries.last())
    #price simulation end
    
    #order calculation start
    current_stock = stock_entries.last()
    orders = Order.objects.filter(end_period_id = current_stock.id)
    
    print("\nprocess\n")
    print(current_stock.id)
    print('\n')
    
    # process orders
    for order in orders:
        print('processing orders')
        order.end_period = current_stock.period
        order.end_period_price = current_stock.price
        user = User.objects.get(id = order.user_id.id)
        
        #case 1 price goes up
        if order.start_period_price < order.end_period_price and order.order_side:
          order.order_result = True
          order.order_final_amount = order.order_amount * .8
        # case 2 price goes down
        elif order.start_period_price > order.end_period_price and not order.order_side:
          order.order_result = True
          order.order_final_amount = order.order_amount * .8
        # case 3 price remains same
        elif order.start_period_price == order.end_period_price:
          order.order_result = True
          order.order_final_amount = order.order_amount * .8
        else:
          order.order_result = False
          order_final_amount = 0
        
        
        user.balance = user.balance + order.order_final_amount
        
        order.order_status = True
        order.save()
        user.save()
        

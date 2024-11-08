from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import time 
import math
from fxsimulator.models import Stock, Order, User
from django.core.cache import cache

channel_layer = get_channel_layer()
room_id = "fxupdateroom"


@shared_task
def stockSimulator():
    #price simulation start
    try:
        last_stock_price = Stock.objects.all().order_by('-period')[0:1].get().price
    except:
        print("no previous data")
        last_stock_price = 300
    
    #variables for simulating GBM
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
    for order in orders:
        print('processing orders')
        order.end_period = current_stock.period
        order.end_period_price = current_stock.price
        user = User.objects.get(id = order.user_id.id)
        
        #side up
        if order.order_side:
            #picked up and profit
            if order.start_period_price < order.end_period_price:
                order.order_result = True
            #picked up and loss
            else:
                order.order_result = False
            #up ratio
            value_change_ratio =  order.end_period_price / order.start_period_price
        #side down 
        else:
            #picked down and profit
            if order.start_period_price > order.end_period_price:
                order.order_result = True
            #picked down and loss
            else:
                order.order_result = False
            #down ratio
            value_change_ratio =  order.start_period_price / order.end_period_price
        
        #final amount calculation after closing 
        if order.order_result:
            order.order_final_amount = order.order_amount * value_change_ratio
        else:
            order.order_final_amount = order.order_amount / value_change_ratio
            
        order.order_diff = order.order_final_amount - order.order_amount
        
        user.balance = user.balance + order.order_final_amount
        
        order.order_status = True
        order.save()
        user.save()
        
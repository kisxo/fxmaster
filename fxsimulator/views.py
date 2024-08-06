from django.shortcuts import render
from django.core.cache import cache
from fxsimulator.models import Stock,Order
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from .models import User
import json
from django.forms.models import model_to_dict


def index(request):
    return render(request, "fxsimulator/index.html")

# Create your views here.
@login_required
def fxtrade(request):
    stock_data = cache.get("stock_data")

    if stock_data is None:
        #query fresh data from database
        stock_entries = Stock.objects.all()
        #format query data as per highcharts
        stock_data = [[entry.period, entry.price] for entry in stock_entries]
        #store the formated data in cache
        cache.set("stock_data", stock_data, 5)

    return render(request, "fxsimulator/tradelive.html", {"stock_data": stock_data})

@login_required
def profile(request):
    return render(request, "fxsimulator/profile.html")

@login_required
def fxorder(request):
    if request.method != "POST" or not request.POST:
        return HttpResponseBadRequest()
    
    in_order_data = json.loads(request.body.decode())
    
    
    in_order_duration = int(in_order_data.get('time', -1))
    in_order_side = in_order_data.get('side', -1)
    in_order_amount = int(in_order_data.get('amount', -1))
    current_stock_data = cache.get("current_stock")
    current_user = User.objects.get(id = request.user.id)
    
    
    if in_order_duration < 1 or in_order_duration > 5 or type(in_order_side) != bool or in_order_amount < 10 or in_order_amount > 10000 or not current_stock_data:
        return HttpResponseBadRequest()
    
    if in_order_amount > current_user.balance:
        return JsonResponse({ 'status': 'Insufficient Balance', 'balance': current_user.balance})
    else:
        current_user.balance = current_user.balance - in_order_amount
        current_user.save()
    
    in_end_period_id = current_stock_data.id + (12 * in_order_duration)# 60 sec / 5 sec = 12 sec. Multiply every minute by 12
    in_end_period = current_stock_data.period + (60000 * in_order_duration)# 1000 millisec = 1 sec. 60,000 = 1 min
    
    current_order= Order.objects.create(user_id = current_user, order_duration = in_order_duration, order_side = in_order_side, order_amount = in_order_amount, start_period_id = current_stock_data.id, start_period = current_stock_data.period, start_period_price = current_stock_data.price, end_period_id = in_end_period_id, end_period = in_end_period)
    current_order_json = model_to_dict(current_order)
    return JsonResponse({ 'status': 'success', 'balance': current_user.balance, 'order': current_order_json})

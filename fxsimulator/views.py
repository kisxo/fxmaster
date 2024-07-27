from django.shortcuts import render
from django.core.cache import cache
from fxsimulator.models import Stock

# Create your views here.
def index(request):
    stock_data = cache.get("stock_data")

    if stock_data is None:
        #query fresh data from database
        stock_entries = Stock.objects.all()
        #format query data as per highcharts
        stock_data = [[entry.period, entry.price] for entry in stock_entries]
        #store the formated data in cache
        cache.set("stock_data", stock_data, 5)

    return render(request, "fxsimulator/tradelive.html", {"stock_data": stock_data})

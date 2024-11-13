from rest_framework import serializers
from django.core.cache import cache
from .models import Order, User

class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model = Order
    fields = '__all__'
    
  # funtion set all fields read-only except some fields
  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      # Set all fields to read-only by default
      for field_name, field in self.fields.items():
          field.read_only = True
      
      write_fields = ['duration', 'side', 'amount']
      for field_name in write_fields:
        self.fields[field_name].read_only = False

  def create(self, data):
    current_stock_data = cache.get("current_stock")
    
    #TODO select current auth user 
    data['user'] = User.objects.get(id = 1)
    data['profit_margin'] = 80
    
    data['opening_id'] = current_stock_data.id
    data['opening_period'] = current_stock_data.period
    data['opening_price'] = current_stock_data.price
    data['closing_id'] = current_stock_data.id + (12 * data['duration'])# 60 sec / 5 sec = 12 sec. Multiply every minute by 12
    order = Order.objects.create(**data)
    
    return data
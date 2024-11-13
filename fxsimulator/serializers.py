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

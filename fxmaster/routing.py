from django.urls import re_path

from fxmaster.consumers import fxConsumer

websocket_urlpatterns = [
    re_path(r"ws/fxupdatechannel/(?P<room_name>\w+)/$", fxConsumer.as_asgi()),
]

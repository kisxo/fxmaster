from celery import shared_task


@shared_task
def add(x, y):
    result = x + y
    print(result)
    return result

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random
import time 

@shared_task
def sendUpdate():
    channel_layer = get_channel_layer()
    room_id = "fxupdateroom"
    period = int(time.time() * 1000)
    price = int(random.random() * 1000)

    async_to_sync(channel_layer.group_send)(
        room_id,
        {
            "type": "fxupdate",
            "data": {
                "period": period,
                "price": price,
            },
        }
    )

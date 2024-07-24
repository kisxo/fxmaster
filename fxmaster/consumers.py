import json
from channels.generic.websocket import AsyncWebsocketConsumer

class fxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.room_name
        # Join room group_adp
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        
        print(self.room_group_name)
        print(self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Code to run when the server receives a message from the WebSocket.
        pass
    
    async def fxupdate(self, event):
        # Code to run when the server send message to the WebSocket.
        
        print(event)
        await self.send(text_data=json.dumps(event))

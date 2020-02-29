from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        payload = json.loads(text_data)
        message = payload["message"]

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": message, "sender": self.scope["user"].username},
        )

    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        self.send(text_data=json.dumps({"message": message, "sender": sender}))

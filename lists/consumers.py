import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from django.utils import timezone


class TodoListConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"todogroup{self.room_name}"

        # Join todolist group for real-time communication
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass

    def send_chat_message(self, message):

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        self.send_chat_message(text_data_json)

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))

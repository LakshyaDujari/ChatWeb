from channels.generic.websocket import WebsocketConsumer
from messaging import models as messaging_models
from login.models import User
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        token = self.get_token_from_scope(self.scope)
        group_name = self.scope['url_route']['kwargs']['group_name']
        username = self.scope['url_route']['kwargs']['user_name']
        self.group_name = group_name
        self.user = User.objects.get(username=username)
        self.chat_room = messaging_models.MessageGroup.objects.get(group_name=self.group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chat_room,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_room,
            self.channel_name
        )
        pass

    def receive(self, text_data = None):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                msg = text_data_json['body']
                message = messaging_models.Message.objects.create(
                    author=self.user,
                    group=self.chat_room,
                    body=msg,
                )
                context = {
                    'author': message,
                    'user': self.user,
                }
                self.send(text_data=context)
                # Process the JSON data here
                event = {
                    'type': 'msg_handler',
                    'message_id': message.id,
                }
                async_to_sync(self.channel_layer.group_send)(
                    self.chat_room,event
                )
            except json.JSONDecodeError:
                # Handle the error (e.g., log it, send an error message back to the client)
                pass
        else:
            # Handle the case where text_data is empty
            pass
    def message_handler(self, event):
        message_id = event['message_id']
        message = messaging_models.Message.objects.get(id=message_id)
        context = {
            'author': message,
            'user': self.user,
            'timestamp': message.timestamp,
        }
        self.send(text_data=context)
        
    def get_token_from_scope(self,scope):
    # Iterate over headers in the scope
        for header in scope['headers']:
            # Decode header name and value from bytes to string
            name, value = header[0].decode(), header[1].decode()
            # Check if this is the Authorization header
            if name == 'authorization':
                # Assuming the header is in the format "Bearer <token>", split and return the token
                token = value.split(' ')[1]
                return token
        return None

from channels.generic.websocket import WebsocketConsumer
from messaging import models as messaging_models
from login.models import User
from asgiref.sync import async_to_sync
import json
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
import re

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        query_string = self.scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        if not token:
            self.close()
            return
        info = AccessToken(token)
        self.user = User.objects.get(id=info.payload['user_id'])
        group_name = self.scope['url_route']['kwargs']['group_name']
        self.group_name = group_name
        # Validate group name
        if not re.match(r'^[a-zA-Z0-9._-]{1,100}$', group_name):
            self.close()
            return
        self.chat_room = messaging_models.MessageGroup.objects.get(group_name=self.group_name).group_name
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
                group_instance = messaging_models.MessageGroup.objects.get(group_name=self.group_name)
                message = messaging_models.Message.objects.create(
                    author=self.user,
                    group=group_instance,
                    body=msg,
                )
                context = {
                    'author': message.author.id,
                    'user': self.user.id,
                    'body': message.body,
                }
                self.send(text_data=json.dumps(context))
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
    def msg_handler(self, event):
        message_id = event['message_id']
        message = messaging_models.Message.objects.get(id=message_id)
        context = {
            'message': message.body,
            'author': message.author.username,
            'user': self.user.username,
            'timestamp': message.timestamp.isoformat(),
        }
        self.send(text_data=json.dumps(context))
        
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

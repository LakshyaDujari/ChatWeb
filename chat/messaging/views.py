from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from login import views as loginviews
from django.contrib.auth.decorators import login_required
import uuid
from messaging.models import *
# Create your views here.
# Create a dictionary to store connected clients

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def get_group_chat(request):
    auth_verify = loginviews.valid_user(request)
    if(auth_verify[0] == False):
        return auth_verify[1]
    if(request.data.get('group_name') == None):
        return Response({'error': 'Group name is required'}, status=400)
    group_name = MessageGroup.objects.get(group_name=request.data.get('group_name'))
    messages = Message.objects.filter(group=group_name)
    message_data = []
    for message in messages:
        message_data.append({
            'author': message.author.username,
            'body': message.body,
            'timestamp': message.timestamp
        })
    return Response({'messages': message_data}, status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
@login_required
def send_msg2grp(request):
    auth_verify = loginviews.valid_user(request)
    if(auth_verify[0] == False):
        return auth_verify[1]
    if(request.data.get('group_name') == None):
        return Response({'error': 'Group name is required'}, status=400)
    if(request.data.get('message') == None):
        return Response({'error': 'Message is required'}, status=400)
    group_name = MessageGroup.objects.get(group_name=request.data.get('group_name'))
    author = loginviews.get_user_from_token(request)
    body = request.data.get('message')
    Message.objects.create(group=group_name, author=author, body=body)
    return Response({'message': 'Message sent'}, status=200)

def create_message_group():
    group_name = uuid.uuid4()
    MessageGroup.objects.create(group_name=group_name)
    return group_name
    
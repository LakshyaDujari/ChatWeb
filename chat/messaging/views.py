# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from login import views as loginviews
from friend import models as friendmodels
import uuid
from messaging.models import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_group_chat(request):
    if(request.data.get('group_name') == None):
        return Response({'error': 'Group name is required'}, status=400)
    group_name = MessageGroup.objects.get(group_name=request.data.get('group_name'))
    messages = Message.objects.filter(group=group_name).order_by('-timestamp')[:30]
    message_data = []
    for message in messages:
        message_data.append({
            'author': message.author.username,
            'body': message.body,
            'timestamp': message.timestamp
        })
    return Response({'messages': message_data}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_msg2grp(request):
    if(request.data.get('group_name') == None):
        return Response({'error': 'Group name is required'}, status=400)
    if(request.data.get('message') == None):
        return Response({'error': 'Message is required'}, status=400)
    group_name = MessageGroup.objects.get(group_name=request.data.get('group_name'))
    author = request.user
    body = request.data.get('message')
    Message.objects.create(group=group_name, author=author, body=body)
    return Response({'message': 'Message sent'}, status=200)

def create_message_group():
    group_name = uuid.uuid4()
    MessageGroup.objects.create(group_name=group_name)
    return group_name

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_msg_groups(request):
    user = request.user
    all_friends = friendmodels.Friends.objects.filter(user=user, is_active=True)
    group_data = []
    for friend in all_friends:
        group_data.append({
            'group_name': friend.msg_group.group_name,
            'friend': friend.friend.username
        })
    return Response({'groups': group_data}, status=200)
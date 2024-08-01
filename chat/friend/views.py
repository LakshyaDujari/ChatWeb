# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from login.models import User
from friend.models import Friends as FriendsModel
from login import views as loginviews
from django.db.models import Q
from messaging import views as messagingviews
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(request):
    try:
        if(request.data.get('friend_id') == None):
            return Response({'error': 'Friend ID is required'}, status=400)
        friend_id = request.data.get('friend_id')
        user = request.user
        friend = User.objects.get(id=friend_id)
        if(user == friend):
            return Response({'error': 'You cannot add yourself as a friend'}, status=400)
        friend_request = FriendsModel.objects.filter(user=user, friend=friend)
        if friend_request.exists():
            return Response({'error': 'Friend request already sent'}, status=400)
        friend_request = FriendsModel.objects.filter(user=friend, friend=user)
        if friend_request.exists():
            return Response({'error': 'You are already friends'}, status=400)
        FriendsModel.objects.create(user=user, friend=friend)
        return Response({'message': 'Friend request sent'}, status=200)
    except Exception as e:
        return Response({'error': 'Error sending friend request','description':str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend(request):
    try:
        user = request.user
        friends = FriendsModel.objects.filter(user=user, is_active=True)
        friend_data = []
        for friend in friends:
            friend_data.append({
                'friend_id': friend.friend.id,
                'username': friend.friend.username,
                'email': friend.friend.email
            })
        return Response({'friends': friend_data}, status=200)
    except Exception as e:
        return Response({'error': 'Error getting friends','description':str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_request(request):
    try:
        user = request.user
        friends = FriendsModel.objects.filter(friend=user, is_active=False)
        friend_data = []
        for friend in friends:
            friend_data.append({
                'username': friend.user.username,
                'email': friend.user.email,
                'friend_id': friend.user.id
            })
        return Response({'friend_requests': friend_data}, status=200)
    except Exception as e:
        return Response({'error': 'Error getting friend requests','description':str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    try:
        if(request.data.get('friend_id') == None):
            return Response({'error': 'Friend ID is required'}, status=400)
        friend_id = request.data.get('friend_id')
        user = request.user
        friend = User.objects.get(id=friend_id)
        friend_request = FriendsModel.objects.filter(user=friend, friend=user, is_active=False)
        if not friend_request.exists():
            return Response({'error': 'No friend request found'}, status=400)
        msg_group = messagingviews.create_message_group(friend_request)
        friend_request.update(is_active = True,msg_group=msg_group.id)
        return Response({'message': 'Friend request accepted'}, status=200)
    except Exception as e:
        return Response({'error': 'Error accepting friend request','description':str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    try:
        friend_id = request.data.get('friend_id')
        if(friend_id == None):
            return Response({'error': 'Friend ID is required'}, status=400)
        user = request.user
        friend = User.objects.get(username=friend_id)
        friend_request = FriendsModel.objects.filter(user=friend, friend=user, is_active=False)
        if not friend_request.exists():
            return Response({'error': 'No friend request found'}, status=400)
        friend_request.delete()
        return Response({'message': 'Friend request rejected'}, status=200)
    except Exception as e:
        return Response({'error': 'Error rejecting friend request','description':str(e)}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfriend(request):
    try:
        friend_id = request.data.get('friend_id')
        if(friend_id == None):
            return Response({'error': 'Friend ID is required'}, status=400)
        user = request.user
        friend = User.objects.get(id=friend_id)
        friend_request = FriendsModel.objects.filter(user=user, friend=friend, is_active=True)
        if not friend_request.exists():
            return Response({'error': 'No friend found'}, status=400)
        friend_request.delete()
        return Response({'message': 'Friend removed'}, status=200)
    except Exception as e:
        return Response({'error': 'Error removing friend','description':str(e)}, status=400)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    try:
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                'username': user.username,
                'first_name': user.userdetail.first_name,
                'bio': user.userdetail.bio,
                'image': user.userdetail.image,
                'email': user.email
            })
        return Response({'users': user_data}, status=200)
    except Exception as e:
        return Response({'error': 'Error getting users','description':str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_friends(request):
    try:
        user = request.user
        friends = FriendsModel.objects.filter(
            Q(user=user, is_active=True) | Q(friend=user, is_active=True)
        )
        friend_data = []
        for friend in friends:
            friend_data.append({
                'friend_id': friend.friend.id,
                'username': friend.friend.username,
                'email': friend.friend.email
            })
        return Response({'friends': friend_data}, status=200)
    except Exception as e:
        return Response({'error': 'Error getting friends','description':str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user_name = request.GET.get('user_name')
        users = User.objects.filter(username__icontains=user_name)
        user_data = []
        for user in users:
            user_data.append({
                'username': user.username,
                'first_name': user.userdetail.first_name,
                'bio': user.userdetail.bio,
                'image': user.userdetail.image,
                'email': user.email
            })
        return Response({'users': user_data}, status=200)
    except Exception as e:
        return Response({'error': 'Error getting user','description':str(e)}, status=400)
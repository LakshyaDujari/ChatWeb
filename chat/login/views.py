from time import timezone
from rest_framework_simplejwt.views import TokenRefreshView
from friend.models import Friends as friend_models
from login.models import User
from login.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken,OutstandingToken,BlacklistedToken
import json

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny,])
    serializer_class = RegisterSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(request):
    return Response({'message': 'Hello, World!' + request.user.username})
# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh_token"]
        rtoken = RefreshToken(refresh_token)
        rtoken.blacklist()
        return Response({'message': 'User logged out successfully'},200)
    except Exception as e:
        return Response({'error': 'User not Authorized','description':str(e)}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_list(request):
    try:
        search_query = request.data.get('search_query')
        if search_query:
            users = User.objects.filter(username__icontains=search_query)
            main_user = request.user
            user_list = []
            for user in users:
                isfriend = False
                try:
                    isfriend = friend_models.Friends.objects.get(user=main_user, friend=user).is_active
                except:
                    isfriend = False
                    
                user_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'fullname':user.userdetail.full_name,
                    'phone':user.userdetail.phone,
                    'verified':user.userdetail.verified,
                    'friend': isfriend,
                    'bio': user.userdetail.bio,
                }
                user_list.append(user_data)
            return Response(user_list, status=200)
        else:
            return Response({'error': 'Search query is required'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
def blacklist_access_token(jti):
    token = OutstandingToken.objects.get(jti=jti)
    token.expires_at = timezone.now()
    BlacklistedToken.objects.create(token=token,blacklisted_at=timezone.now())
    return True
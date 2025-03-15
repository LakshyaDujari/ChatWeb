from time import timezone
from rest_framework_simplejwt.views import TokenRefreshView
from friend.models import Friends as friend_models
from login.models import User,OTP
from login.serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken,OutstandingToken,BlacklistedToken
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import time

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = ([AllowAny,])
    serializer_class = RegisterSerializer
# OTP Expiry Time
OTP_EXPIRY_TIME = 300 # 5 minutes
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

@api_view(['POST'])
def forgotPassword(request):
    try:
        email = request.data['email']
        if(email == ''):
            return Response({'error': 'Email is required'}, status=400)
        user = User.objects.get(email=email)
        if(user == None):
            return Response({'error': 'User not found'}, status=400)
        unique_otp = generate_otp(email)
        message = f"Your OTP is {unique_otp} for resetting your password. If you didn't request this, please ignore this email.\n\nlakshya dujari\nChat Box, Dil khol ke likho\nBikaner, Rajasthan 334001\nhttp://Unikonnect.in"
        if(sendMail(email,'Support ChatBox Forgot Password',message)):
            otp = OTP.objects.create(user=user, otp=unique_otp)
            return Response({'message': 'OTP sent successfully'}, status=200)
        else:
            return Response({'error': 'Email not sent'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
def verifyOTP(request):
    try:
        email = request.data['email']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        otp = request.data['otp']
        if(email == '' or new_password == '' or confirm_password == '' or otp == ''):
            return Response({'error': 'Email, Password, Confirm Password and OTP is required'}, status=400)
        user = User.objects.get(email=email)
        if(user == None):
            return Response({'error': 'User not found'}, status=400)
        otp = OTP.objects.get(user=user, otp=otp, is_verified=False)
        if(otp == None):
            return Response({'error': 'Please Enter Valid OTP'}, status=400)
        if(otp.created_at < timezone.now() - timezone.timedelta(seconds=OTP_EXPIRY_TIME)):
            return Response({'error': 'OTP Expired'}, status=400)
        if(new_password != confirm_password):
            return Response({'error': 'Password and Confirm Password does not match'}, status=400)
        otp.is_verified = True
        otp.save()
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password Change Successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

def generate_otp(email):
    characters = string.ascii_letters + string.digits + str(int(time.time())) + email
    otp = ''.join(random.choice(characters) for _ in range(6))
    return otp

def sendMail(user,subject,message):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False
    
def blacklist_access_token(jti):
    token = OutstandingToken.objects.get(jti=jti)
    token.expires_at = timezone.now()
    BlacklistedToken.objects.create(token=token,blacklisted_at=timezone.now())
    return True
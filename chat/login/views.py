import django
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from login import models
from friend import models as friend_models

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    try:
        uname = request.data.get('username')
        password = request.data.get('password')
        if(uname == '' or password == ''):
            return Response({'error': 'All fields are required'}, status=400)
        user = authenticate(request,username=uname, password=password)
        if user is None:
            return Response({'error': 'Invalid Credentials'}, status=400)
        else:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            user_info = models.User.objects.get(username=user.username) 
            models.Session.objects.update_or_create(ip=request.META.get('REMOTE_ADDR'), user=user_info, isActive=True, sessionId= django.middleware.csrf.get_token(request), token=token)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
                'temp':django.middleware.csrf.get_token(request)
                # Include any other fields you want to return
            }
            return Response(user_data, status=200)
    except:
        return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
def logout_user(request):
    try:
        logout(request)
        models.Session.objects.get(token=request.headers.get('Authorization').split(' ')[1]).delete()
        return Response({'message': 'User logged out successfully'},200)
    except:
        return Response({'error': 'User not Authorized'}, status=400)
    
@api_view(['POST'])
def create_user(request):
    try:
        uname = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone = request.data.get('phone')
        name = request.data.get('name')
        if(uname == '' or uname == None or email == '' or email == None or password == '' or password == None or phone == '' or phone == None or name == '' or name == None):
            return Response({'error': 'All fields are required'}, status=400)
        if User.objects.filter(username=uname).exists():
            return Response({'error': 'Username already exists'}, status=400)   
        user = User.objects.create_user(uname, email, password)
        user.save()
        models.User.objects.create(username=uname, email=email, password=password, phone=phone, name=name)
        
        return Response({'message': 'User created successfully'})
    except:
        return Response({'error': 'Invalid Credentials'}, status=400)

@api_view(['POST'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
def get_user_list(request):
    try:
        auth_verify = valid_user(request)
        if(auth_verify[0] == False):
            return auth_verify[1]
        search_query = request.data.get('search_query')
        if search_query:
            users = User.objects.filter(username__icontains=search_query)
            main_user = get_user_from_token(request)
            user_list = []
            for user in users:
                isfriend = False
                try:
                    isfriend = friend_models.Friends.objects.get(user=main_user, friend=user).is_active
                except:
                    isfriend = False
                    
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'friend': isfriend,
                }
                user_list.append(user_data)
            return Response(user_list, status=200)
        else:
            return Response({'error': 'Search query is required'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

def valid_user(request):
    if(request.headers.get('Authorization') == None):
        return False,Response({'error': 'Authorization header is required'}, status=400)
    token = request.headers.get('Authorization').split(' ')[1]
    session_data = models.Session.objects.get(token=token)
    if(session_data and session_data.isActive and session_data.ip == request.META.get('REMOTE_ADDR')):
        return True,session_data.user
    else: 
        return False,Response({'error': 'User not Authorized'}, status=400)
    
def get_user_from_token(request):
    token = request.headers.get('Authorization').split(' ')[1]
    session_data = models.Session.objects.get(token=token)
    user = User.objects.get(username=session_data.user.username)
    return user
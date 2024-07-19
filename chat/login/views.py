from django.http import HttpResponseBadRequest
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from login import models

@api_view(['GET'])
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request):
    token = request.auth.credentials.get('Token')
    return Response({'message': 'Hello, world!'})


@api_view(['POST'])
def login2(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # Check if the user exists in the database
    try:
        user_info = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest("User information not found")
    if password == user_info.password:
        # token, _ = Token.objects.get_or_create(user_info)
        token = Token.generate_key()
        models.Session.objects.create(ip=request.META.get('REMOTE_ADDR'), user=user_info, isActive=True, sessionId=token)
        request.user = user_info
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)
    
    
def validate_token(token):
    session = models.Session.objects.get(token=token)
    if session:
        return True
    else:
        return False


@api_view(['POST'])
def login_user(request):
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
        models.Session.objects.create(ip=request.META.get('REMOTE_ADDR'), user=user.username, isActive=True, sessionId=token)
    return Response({'message': 'User logged in successfully','userInfo':user},200)

def logout_user(request):
    logout(request)
    return Response({'message': 'User logged out successfully'},200)

@api_view(['POST'])
def create_user(request):
    uname = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone')
    name = request.data.get('name')
    if(uname == '' or email == '' or password == '' or phone == '' or name == ''):
        return Response({'error': 'All fields are required'}, status=400)
    if User.objects.filter(username=uname).exists():
        return Response({'error': 'Username already exists'}, status=400)   
    user = User.objects.create_user(uname, email, password)
    user.save()
    models.User.objects.create(username=uname, email=email, password=password, phone=phone, name=name)
    
    return Response({'message': 'User created successfully'})

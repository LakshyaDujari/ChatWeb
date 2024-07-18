from django.http import HttpResponseBadRequest
from django.shortcuts import render
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
    return Response({'message': 'Hello, world!'})


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    # Check if the user exists in the database
    try:
        user_info = models.User.objects.get(user=username)
    except models.User.DoesNotExist:
        return HttpResponseBadRequest("User information not found")
    if password == user_info.password:
        token, _ = Token.objects.get_or_create(user=username)
        models.Session.objects.create(ip=request.META.get('REMOTE_ADDR'), token=token, user=user_info, isActive=True, sessionId=token.key)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)
    
    
def validate_token(token):
    session = Session.query.filter_by(token=token).first()
    if session:
        return True
    else:
        return False


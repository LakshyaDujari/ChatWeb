from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from login import views as loginviews
import asyncio
import websockets
# Create your views here.
# Create a dictionary to store connected clients
connected_clients = {}

# Define the WebSocket endpoint
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
async def websocket_endpoint(request):
    auth_verify = loginviews.valid_user(request)[0]
    if(auth_verify[0] == False):
        return auth_verify[1]
    # Upgrade the HTTP request to a WebSocket connection
    websocket = await websockets.connect('ws://' + request.get_host() + request.path)

    # Store the WebSocket connection in the dictionary
    connected_clients[request.user.id] = websocket

    try:
        # Continuously listen for incoming messages
        while True:
            message = await websocket.recv()
            # Process the received message (e.g., send it to other clients)
            await process_message(request.user.id, message)
    finally:
        # Remove the WebSocket connection from the dictionary when the connection is closed
        del connected_clients[request.user.id]

# Function to process the received message
async def process_message(sender_id, message):
    # Iterate over the connected clients
    for client_id, websocket in connected_clients.items():
        # Send the message to all clients except the sender
        if client_id != sender_id:
            await websocket.send(message)



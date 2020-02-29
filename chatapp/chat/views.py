import json
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt


def index(request):
    authenticate(request, username="dexter", password="admin")
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@csrf_exempt
def trigger(request):
    payload = json.loads(request.body)
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        "chat_" + payload["room"],
        {
            "type": "chat_message",
            "message": payload["message"],
            "sender": "robot"
        }
    )
    return JsonResponse({"result": "ok"})

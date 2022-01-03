from django.shortcuts import render
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/')
def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


@login_required(login_url='/')
def send(request):
    message = request.POST['message']
    user = request.user
    name = user.first_name + " " + user.last_name
    room_id = request.POST['room_id']
    room = Room.objects.get(pk=room_id)

    new_message = Message.objects.create(value=message, user=user, username=name, room=room)
    new_message.save()
    return HttpResponse('Message sent successfully')


@login_required(login_url='/')
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})

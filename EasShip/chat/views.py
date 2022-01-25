from django.shortcuts import render
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Customer.models import customer, Customer_profile
from PatnerCompany.models import patnerComp, Comp_profile


# Create your views here.
@login_required(login_url='/')
def room(request, room):
    user = request.user
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat/room.html', {
        'user': user,
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
    muser = []
    image = []
    room_details = Room.objects.get(name=room)
    useronline = request.user
    messages = Message.objects.filter(room=room_details.id)
    for m in messages:
        muser.append(m.user.user_name)
        if m.user.is_customer:
            c = customer.objects.get(user=m.user)
            cp = Customer_profile.objects.get(cust=c)
            image.append(cp.company_logo.url)
        elif m.user.is_company:
            p = patnerComp.objects.get(user=m.user)
            pp = Comp_profile.objects.get(comp=p)
            image.append(pp.company_logo.url)

    return JsonResponse(
        {"messages": list(messages.values()), "image": image, "muser": muser, "Ruser": useronline.user_name})

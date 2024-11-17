import hashlib
from django.shortcuts import get_object_or_404, render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')# get the username
    room_details = Room.objects.get(name=room)# get the room details
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details # pass the room details to the room.html
    })

def checkview(request):
    room= request.POST['room_name']
    username= request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)
    
    
# def checkview(request):
#     room = request.POST['room_name']
#     username = request.POST['username']

#     if Room.objects.filter(name=room).exists():
#         return redirect(f'/{room}/?username={username}')
#     else:
#         new_room = Room.objects.create(name=room)
#         new_room.save()
#         return redirect(f'/{room}/?username={username}')

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

from django.http import JsonResponse
from .models import Room, Message

def getMessages(request, room):
    # Récupérer les détails de la salle
    room_details = Room.objects.get(name=room)
    
    # Filtrer les messages correspondant à cette salle
    messages = Message.objects.filter(room=room_details.id).values()
    
    # Ajouter une clé "is_current_user" à chaque message
    enriched_messages = []
    for message in messages:
        message = dict(message)
        message["is_current_user"] = message["user"] == request.user.username
        # Générer une couleur unique à partir du nom d'utilisateur
        user_color = "#" + hashlib.md5(message["user"].encode()).hexdigest()[:6]
        message["user_color"] = user_color
        enriched_messages.append(message)
    
    # Retourner les messages enrichis
    return JsonResponse({"messages": enriched_messages})

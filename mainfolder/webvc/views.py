from django.shortcuts import render

# Create your views here.

def room(request):

    return render(request,'webvc/room.html')


def lobby(request):
    return render(request,'webvc/lobby.html')
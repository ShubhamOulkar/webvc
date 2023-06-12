from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random 
import time
import json
from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#Build token with uid
def getToken(request):
    appId = '4c883b025263435eae98296fcaabc6cf'
    appCertificate = 'a58f1f9a36d74146919359227c39bce8'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    tokenexpirationtime = 3600 * 24
    currentTime = time.time()
    privilegeExpiredTs = currentTime + tokenexpirationtime
    role = 1 # host 2=guest
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid},safe=False)


def room(request):

    return render(request,'webvc/room.html')


def lobby(request):
    return render(request,'webvc/lobby.html')

@csrf_exempt
def createuser(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)


def getmember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(uid=uid, room_name=room_name)

    name = member.name
    return JsonResponse({'name':name}, safe=False)
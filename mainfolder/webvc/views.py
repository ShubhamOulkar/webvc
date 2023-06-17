from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random 
import time
import re
import json
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


def start(request):
    return render(request, 'webvc/getin.html')


#Build token with uid
@login_required(login_url="/login/")
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


@login_required(login_url="/login/")
def room(request):
    return render(request,'webvc/room.html')

@login_required(login_url="/login/")
def lobby(request):
    return render(request,'webvc/lobby.html')


# def createuser(request):
#     data = json.loads(request.body)
#     member, created = RoomMember.objects.get_or_create(
#         name = data['name'],
#         uid=data['UID'],
#         room_name=data['room_name']
#     )
#     return JsonResponse({'name':data['name']}, safe=False)


# def getmember(request):
#     uid = request.GET.get('UID')
#     room_name = request.GET.get('room_name')

#     member = RoomMember.objects.get(uid=uid, room_name=room_name)

#     name = member.name
#     return JsonResponse({'name':name}, safe=False)


def login_view(request):
    if request.method == 'POST':
        if request.POST['check-mark'] == 'on':
            email_username = request.POST["email-username"]
            password = request.POST["password"]

            # check if email_username is an email or username
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_username):
                # get an username for an email
                try:
                    username = User.objects.get(email=email_username)
                    user = authenticate(request, username=username.username, password=password)

                    if user is None:
                    # check why none ? because of username or password
                        if not username.check_password(password):
                            messages.error(request, "Password is incorrect.")
    
                except User.DoesNotExist:
                    user = None
                    messages.error(request, "Email does not exist")
            else :
                try:
                    username = User.objects.get(username=email_username)
                    user = authenticate(request, username=email_username, password=password)

                    if user is None:
                    # check why none ? because of username or password
                        if not username.check_password(password):
                            messages.error(request, "Password is incorrect.")
                            
                except User.DoesNotExist:
                    user = None
                    messages.error(request, "Username does not exist")
                
                
            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("lobby"))
            else:
                return HttpResponseRedirect(reverse("start"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("start"))


def signup(request):
    return render(request, 'webvc/signup.html')

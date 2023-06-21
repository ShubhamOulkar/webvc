from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import random 
import time
import re
import json
from .models import *

number_list = [0,1, 2, 3, 4, 5, 6, 7, 8, 9 ]


def start(request):
    if not request.user.is_authenticated:
        return render(request, 'webvc/getin.html')
    else:
        return render(request, 'webvc/hostVC.html',{'username':request.user.username})


#Build token with uid
@login_required(login_url="/start/")
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


@login_required(login_url="/start/")
def room(request):
    return render(request,'webvc/room.html')

@login_required(login_url="/start/")
def hostVC(request):
    return render(request,'webvc/hostVC.html',{'username':request.user.username})


def savechannel(request):
    data = json.loads(request.body)
    member, created = VideoConferenceRecord.objects.get_or_create(
        created_by = User.objects.get(username=data['name']),
        uid=data['UID'],
        room_name=data['room_name']
    )
    return JsonResponse({'name':data['name']}, safe=False)


def joinmember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = VideoConferenceRecord.objects.get(uid=uid, room_name=room_name)

    name = member.created_by.username

    return JsonResponse({'name':name}, safe=False)


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
                    username = User.objects.get(username=email_username.lower())
                    user = authenticate(request, username=email_username.lower(), password=password)
                   
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
            return HttpResponseRedirect(reverse("vcRoom"))
        else:
            return HttpResponseRedirect(reverse("start"))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("start"))


# API -> send email for verification
def send_email(request):
    if request.method == 'POST':
        email = json.loads(request.body)
        subject = 'webVC Reset Password varification'
        global code
        code = random.choices(number_list, k=6)
        # check email exist or not
        to_email = email['email']
        try:
            email = User.objects.get(email=to_email)
        except User.DoesNotExist:
            to_email = False
            message = "Following email is not valid."
            
        from_email = settings.EMAIL_HOST_USER
        if subject and code and to_email:
            try:
                send_mail(subject, ''.join(map(str,code)), from_email, [to_email])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            message = "verification code is send to following email." 
            return JsonResponse({'message':message, 'email':to_email}, safe=False)      
    return render(request, 'webvc/forgetpassword.html')
        

# API -> verify user received code
def verify_code(request):
    if request.method == 'POST':
        code0 = json.loads(request.body)
        
        if code0['code'] == ''.join(map(str,code)):
            message = "verification is done! now set your password for following email."
            status = True
        else:
            message = "verification failed! for following email."
            status = False
            return JsonResponse({'message':message,'email':code0['email'], 'status':status}, safe=False)
        return JsonResponse({'message':message,'email':code0['email']}, safe=False) 


# API -> reset and save new password
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data['password']
        user = User.objects.get(email=data['email'])
        user.set_password(password)
        user.save()
    return JsonResponse({'message':'Password Saved, try login for following email'}, safe=False)


def signup(request):
    if request.method == "POST":
        if request.POST['check-mark'] == 'on':
            username = request.POST["username"].lower()
            email = request.POST["email"]
            
            # Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                messages.error(request, 'Password must match')
                return render(request, "webvc/getin.html")

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password) # type: ignore
                user.save()
            except IntegrityError:
                messages.error(request, 'Username / Email Already taken.')
                return render(request, "webvc/getin.html")

            login(request, user)
            return HttpResponseRedirect(reverse("vcRoom"))
    else:
        return HttpResponseRedirect(reverse("start"))

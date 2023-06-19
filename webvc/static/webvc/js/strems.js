const APP_ID = '4c883b025263435eae98296fcaabc6cf'
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))
let NAME = sessionStorage.getItem('name')
const CSRF_TOKEN = getCookie('csrftoken')

// script for Display video source to a page
const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL;

    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try {
        await client.join(APP_ID, CHANNEL, TOKEN, UID)
    }catch(error){
        console.error(error)
        window.open('/vcRoom/','_self')
    }

   localTracks = await  AgoraRTC.createMicrophoneAndCameraTracks()

   let creator = await savechannel()

   let player = `<div class="video-container" id="user-container-${UID}">
                <div class="username-wrapper"><span class="user-name">${creator.name}</span></div>
                <div class="video-player" id="user-${UID}"></div>
                </div>`

    document.getElementById('video-strems').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0],localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }

        let joining = await joinmember(user)

        player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="username-wrapper"><span class="user-name">${joining.name}</span></div>
            <div class="video-player" id="user-${user.uid}"></div>
            </div>`

        document.querySelector('#video-strems').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio'){
        user.audioTrack.play()
    }
}


let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}


let leaveAndRemoveLocalStream = async () => {
    for (let i = 0 ; localTracks.length >i ; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }
    await client.leave()
    window.open('/vcRoom/', '_self')
}

let toggleCamera = async (e) => {
    if (localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style.color = '#000'
    }else {
        await localTracks[1].setMuted(true)
        e.target.style.color = '#fff'
    }
}


let micToggle = async (e) => {
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.color = '#000'
    }else {
        await localTracks[0].setMuted(true)
        e.target.style.color = '#fff'
    }
}


// Get csrf token 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


let savechannel = async () => {
    let response = await fetch('/savechannel/', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': CSRF_TOKEN  
        },
        mode: 'same-origin' ,
        body:JSON.stringify({
            'name': NAME,
            'room_name': CHANNEL,
            'UID':UID
        })
    })
    let member = await response.json()
    return member
}

let joinmember = async (user) => {
    let response = await fetch(`/join_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    .catch(err => console.log(err))
    let member = await response.json()
    return member
}


// Script for login and sign up page

function login(){
    document.querySelector('#welcome-container').style.display = 'none';
    document.querySelector('#login-page').style.display = 'block';
    document.querySelector('#signup-page').style.display = 'none';
}

function signup(){
    document.querySelector('#welcome-container').style.display = 'none';
    document.querySelector('#login-page').style.display = 'none';
    document.querySelector('#signup-page').style.display = 'block';
}

function check_password(){
    password =  document.querySelector('#password').value;
    confirmation =  document.querySelector('#confirmation').value;

    if (password === confirmation){
        document.querySelector('#correct-password-label').style.display = 'block';
        document.querySelector('#incorrect-password-label').style.display = 'none';
    }else{
        document.querySelector('#incorrect-password-label').style.display = 'block';
        document.querySelector('#correct-password-label').style.display = 'none';
    }
}


joinAndDisplayLocalStream()

document.getElementById('leave-but').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('video-but').addEventListener('click', toggleCamera)
document.getElementById('mic-but').addEventListener('click', micToggle)

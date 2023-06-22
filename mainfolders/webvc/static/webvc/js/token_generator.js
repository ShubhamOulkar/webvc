// This script will generate new token with new channel name 

let form = document.getElementById('form')

    let handleSubmit = async (e) => {
        e.preventDefault()
        let room = e.target.room.value
        let name = e.target.username.value

        // fetch API to generate channel from django
        let response = await fetch(`/get_token/?channel=${room}`)
        let data = await response.json()

        let uid = data.uid
        let token = data.token

        // store in browser session storage 
        sessionStorage.setItem('UID', uid)
        sessionStorage.setItem('token', token)
        sessionStorage.setItem('room', room)
        sessionStorage.setItem('name', name)

        window.open('/room/', '_self')
    }

    form.addEventListener('submit', handleSubmit)

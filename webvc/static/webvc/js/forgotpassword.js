 // get an email from input and send to the server, return rsponse from server
 document.getElementById('send-email').addEventListener('submit', async (e) => {
    e.preventDefault()
    document.getElementById('verify-code').style.display = 'block';
    document.getElementById('send-email').style.display = 'none';
    document.getElementById('reset-password').style.display = 'none';

    let response = await fetch('/send_email/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN
      },
      mode: 'same-origin',
      body: JSON.stringify({
        'email': document.getElementById('from_email').value,
      })
    })
    let msg = await response.json()
    document.querySelector('#message').innerHTML = msg.message;
    document.querySelector('#mail').innerHTML = msg.email;
    if (msg.status === false) {
      document.getElementById('reset-password').style.display = 'none';
      document.getElementById('verify-code').style.display = 'none';
      document.getElementById('send-email').style.display = 'none';
      document.getElementById('redirect-login').style.display = 'block';
    }
  })

  // get code from input and send to server and return response from the server
  document.getElementById('verify-code').addEventListener('submit', async (e) => {
    e.preventDefault()
    document.getElementById('verify-code').style.display = 'none';
    document.getElementById('send-email').style.display = 'none';
    document.getElementById('reset-password').style.display = 'block';

    let response = await fetch('/verify_code/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN
      },
      mode: 'same-origin',
      body: JSON.stringify({
        'code': document.getElementById('code').value,
        'email': document.querySelector('#mail').innerHTML,
      })
    })
    let msg = await response.json()
    document.querySelector('#message').innerHTML = msg.message;
    document.querySelector('#mail').innerHTML = msg.email;
    if (msg.status === false) {
      document.getElementById('reset-password').style.display = 'none';
      document.getElementById('verify-code').style.display = 'none';
      document.getElementById('send-email').style.display = 'none';
      document.getElementById('redirect-login').style.display = 'block';
    }
  })

  // get password and send to server, return response from server
  document.getElementById('reset-password').addEventListener('submit', async (e) => {
    e.preventDefault()
    document.getElementById('verify-code').style.display = 'none';
    document.getElementById('send-email').style.display = 'none';
    document.getElementById('reset-password').style.display = 'none';
    document.getElementById('redirect-login').style.display = 'block';

    let response = await fetch('/reset_password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN
      },
      mode: 'same-origin',
      body: JSON.stringify({
        'password': document.getElementById('confirmation').value,
        'email': document.querySelector('#mail').innerHTML,
      })
    })
    let msg = await response.json()
    document.querySelector('#message').innerHTML = msg.message;
  })
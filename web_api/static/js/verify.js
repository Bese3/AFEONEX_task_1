const uri = "http://localhost:5001/";
const otp = document.querySelector('.form-control.otp')
const sender = document.querySelector('.btn.btn-default')
document.querySelector('button').addEventListener('click', () => {
    event.preventDefault()
});


function setAccessToken(token) {
    try {
        document.cookie = `access_token=;path=/`
        document.cookie = `access_token=${token};path=/`
    } catch (e) {
        console.error('Error saving to cookies:', e);
    }
}

function getAccessToken() {
    const cookieString = document.cookie;
    const cookies = cookieString.split(';');

    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName.trim() === 'access_token') {
            return decodeURIComponent(cookieValue);
        }
    }
    return null; 
}



sender.addEventListener('click', async () => {
    if (otp.value == "") {
        return
    }
    const queryParams = new URLSearchParams(window.location.search);
    const id = queryParams.get('id')
    jsonData = {
        id,
        'otp': otp.value
    }
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }
    await fetch(`${uri}auth/verify-email`, requestOptions)
    .then(res => {
        if (res.ok) {
            return res.json()
        }
    })
    .then(data => {
        if (data.message) {
            location.href = `${uri}auth/login`;
        }
    })
})
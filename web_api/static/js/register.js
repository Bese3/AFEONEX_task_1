const first_name = document.querySelector('.form-control.fname')
const last_name = document.querySelector('.form-control.lname')
const username = document.querySelector('.form-control.uname')
const email = document.querySelector('.form-control.email')
const phone = document.querySelector('.form-control.pnumber')
const password = document.querySelector('.form-control.password')
const uri = "http://localhost:5001/";

const register = document.querySelector('.btn.btn-default.register')
const signin = document.querySelector('.btn.btn-default.sign-in')

document.querySelector('button').addEventListener('click', () => {
    event.preventDefault()
})
signin.addEventListener('click', () => {
    location.href = `${uri}auth/login`;
})


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


register.addEventListener('click', async () => {
    if (first_name.value == "" || last_name.value == "" || username.value == ""  || email.value == "" || phone.value == "" || password.value == ""){
        return
    }
    const jsonData = {
        'first_name': first_name.value,
        'last_name': last_name.value,
        'username': username.value,
        'email': email.value,
        'phone': phone.value,
        'password': password.value
    }
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }
    await fetch(`${uri}/auth/create-account`, requestOptions)
    .then(async (res) => {
        // console(document.querySelector('p.warning'))
        if (res.ok){
            const data = await res.json()
            // console.log(data)
            location.href = `${uri}auth/verify-email?id=${data.id}`;
        } else {
            document.querySelector('p.warning').textContent = '';
            document.querySelector('p.warning').append('Username, email or phone is already registered')
        }

    })
})
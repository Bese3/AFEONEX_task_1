const button = document.querySelector(".btn.btn-default")
const signUp = document.querySelector(".btn.btn-default.sign-up")

button.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the button from performing its default action
});

const uri = "http://localhost:5001/"


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

signUp.addEventListener('click', () => {
    location.href = `${uri}auth/create-account`
})

button.addEventListener('click', async (event) => {
    const username = document.querySelector('.user-name').value;
    const password = document.querySelector('.password').value;
    jsonData = {
        username,
        password
    }
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }
    fetch(`${uri}auth/login`, requestOptions)
    .then(res =>  {
        console.log(res.ok)
        if (res.ok) {
            return res.json(); // Parse the JSON response
        } else {
            throw new Error('Login failed'); // Throw an error for non-200 response
        }
    })
    .then((data) => {
        // Store the access token in localStorage
        setAccessToken(data.token);
        // Redirect to the home page
        
        window.location.href = '/';
    })
    .catch(error => {
        console.error('Login error:', error);
        // Redirect to the login page if login fails
        window.location.href = `/auth/login`;
    });
});

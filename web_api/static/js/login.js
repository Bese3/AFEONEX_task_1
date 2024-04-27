const button = document.querySelector(".btn.btn-default")

button.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent the button from performing its default action
    
    // Optional: You can add custom logic here if needed
    console.log('Button clicked, but no action performed');
});

const uri = "http://localhost:5001/"
const xhr = new XMLHttpRequest();
xhr.open('GET', uri);

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

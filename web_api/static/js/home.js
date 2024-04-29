const uri = "http://localhost:5001/";
const postBtn = document.querySelector('.btn.post')



document.querySelector('button').addEventListener('click', () => {
    event.preventDefault()
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
function deleteAccessToken(){
    try{
        document.cookie =  `access_token=;path=/`
    } catch(e) {
        console.error('Error deleting from cookies:', e);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    try{
        const logout = document.querySelector('.profile-link p.full-name a.logout');
        
        logout.addEventListener('click', () => {
            deleteAccessToken()
        })
    } catch (e) {

    }
});

const post = document.querySelectorAll(".user-content-box")
const tweetsElement = document.querySelectorAll('.tweets');
post.forEach((elem, indx) => {
    elem.addEventListener('click', async () => {
        const postId = tweetsElement[indx].getAttribute('id');
        const userId = tweetsElement[indx].getAttribute('user-id');
        window.location.href = `${uri}post/${postId}/${userId}`;
    
    })
});


postBtn.addEventListener('click', async () => {
    const input = document.getElementById('post-data');
    if (input.value == '') {
        return
    }
    const user = document.querySelector('.profile-link')
    const userId = user.getAttribute('user-id')
    if (userId == ''){
        location.href = `${uri}auth/login`;
    }
    jsonData = {
        'body': input.value
    }
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }
    await fetch(`${uri}post/${userId}`, requestOptions)
    location.reload();

})





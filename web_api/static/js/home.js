const uri = "http://localhost:5001/";


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
})





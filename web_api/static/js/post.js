const button = document.querySelector(".btn.btn-default");
const edit = document.querySelector(".btn.btn-default.edit");
const tweetsElement = document.querySelector('.tweets');
const postId = tweetsElement.getAttribute('id');
const userId = tweetsElement.getAttribute('user-id');
const uri = "http://localhost:5001/";
const logout = document.querySelector('.profile-link p.full-name a.logout');


function deleteAccessToken(){
    try{
        document.cookie =  `access_token=;path=/`
    } catch(e) {
        console.error('Error deleting from cookies:', e);
    }
}

document.querySelector('button').addEventListener('click', () => {
    event.preventDefault()
})

logout.addEventListener('click', () => {
    deleteAccessToken()
})

button.addEventListener('click', async () => {
    const input = document.getElementById('feedBackInput');
    if (input == null || input == ""){
        return
    }
    jsonData = {
        'message': input.value
    }
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    }
    await fetch(`${uri}comment/${postId}`, requestOptions)
    .then((res) => {
        input.value = "";
        location.reload();
    })
    
});

// edit.addEventListener('click', async() => {
// const commentId = edit.getAttribute('id');
// console.log(commentId)
//     const editInput = '<input type="text" id=' + commentId + ' placeholder=Edit Your comment?>'
//     console.log(editInput)
// })
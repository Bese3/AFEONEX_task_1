const button = document.querySelector(".btn.btn-default")
const tweetsElement = document.querySelector('.tweets');
const postId = tweetsElement.getAttribute('id');
const uri = "http://localhost:5001/";

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
        if (res.status == 200){
            window.location.reload();
        }
    })

})
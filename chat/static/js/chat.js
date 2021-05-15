const userList = document.querySelectorAll('.username');
const chatForm = document.getElementById('chat_form');
const content = document.getElementById('content');
const filter = document.getElementById('filter');
const currentUser = document.getElementById('current-user').dataset.currentUser;
let otherUser = document.getElementById('other-user')



filter.addEventListener('input', e=>{
    if(e.target.value.length >= 5){
        fetch('/chat', {data:e.target.value})
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// get selected user from chatlist
let getUser = userList.forEach(user => {
    user.addEventListener('click', e => {
        document.getElementById("myFieldSet").disabled=false
        let data = user.dataset.userId;
        otherUser = data
        console.log(otherUser)
        fetch('/chat/', {
            method: 'POST',
            mode: 'same-origin',

            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                // console.log('Success:', data);
                content.innerHTML = data.map(function (item) {
                    return `<div class="my-4 ${item.user__username === currentUser ? "reciever ms-auto" : "sender me-auto"} w-75">` +
                        '<span>' + item.created + '</span>' + '<br>' +
                        item.text +
                        '</div>';
                }).join('');
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    })
});


chatForm.addEventListener('submit', function (e) {
    e.preventDefault();
    date = moment().startOf().fromNow();
    formData = new FormData(chatForm)
    formData.append('recepient', otherUser);
    const textMessage = formData.get("message")
    content.innerHTML += '<div class="my-4 reciever ms-auto w-75">' +
    '<span>' 
        + date + 
    '</span>' + '<br>' 
        + textMessage +
    '</div>'
    const request = new Request(
        '/save/',
        { headers: { 'X-CSRFToken': csrftoken } }
    );
    fetch(request, {
        method: 'POST',
        mode: 'same-origin',  // Do not send CSRF token to another domain.
        body: formData,
    }).then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            document.getElementById('floatingTextarea').value = ''

        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
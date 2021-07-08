// Function to return cookieValue for csrf token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function likeFunction(id) {
    fetch('/post/like', {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            id: id
        })
    })
        .then(response => response.json())
        .then(result => {

            // Print result to console
            console.log(result);
            let like_count = result.like_count;
            let id = result.id;

            document.querySelector(`#like_display_${id}`).innerHTML = `This post has ${like_count} like!`

        })

    //document.querySelector("#like_display")
    // Prevent submit form on the other pages, only submit on this page
    return false;
}


document.querySelector('#edit').onclick = () => {


}

document.querySelector('#follow').onclick = () => {

}

document.querySelector('#unfollow').onclick = () => {

}
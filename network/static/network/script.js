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

// Function for like button
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


            if (result.message == 'liked.') {
                document.querySelector(`#like_${result.id}`).innerHTML = 'Unlike'
            } else {
                document.querySelector(`#like_${result.id}`).innerHTML = 'Like'
            }
            document.querySelector(`#like_display_${result.id}`).innerHTML = `This post has ${result.like_count} like!`

        })

    // Prevent submit form on the other pages, only submit on this page
    return false;
}


// Function for follow button
function followFunction(id) {
    fetch('/follow', {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result)

        if (result.message == 'followed') {
            document.querySelector('#follow').innerHTML = 'Unfollow';
            document.querySelector('#follower').innerHTML = `This user has ${result.follower_count} followers`;
        } else {
            document.querySelector('#follow').innerHTML = 'Follow';
            document.querySelector('#follower').innerHTML = `This user has ${result.follower_count} followers`;
        }
    })
}

// Function for edit button
function editFunction(id) {
    document.querySelector(`#content_${id}`).hidden = true;
    document.querySelector(`#edittext_${id}`).hidden = false;
    document.querySelector(`#save_${id}`).hidden = false;
}


// Function for save the change after edit
function saveFunction(id) {

    const new_content = document.querySelector(`#edittext_${id}`).value;
    document.querySelector(`#content_${id}`).innerHTML = new_content;

    fetch('/post/edit', {
        method: 'POST',
        headers: {"X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            id: id,
            content: new_content
        })
    })
    .then(response => response.json())
    .then(result => console.log(result))

    document.querySelector(`#content_${id}`).hidden = false;
    document.querySelector(`#edittext_${id}`).hidden = true;
    document.querySelector(`#save_${id}`).hidden = true;
}

document.addEventListener('DOMContentLoaded', function() {

    // Navigation Buttons
    document.querySelector('#all').addEventListener('click', load_all_posts);
    document.querySelector('#following').addEventListener('click', load_following_posts);
    current_user = document.querySelector('#user').dataset.username;
    document.querySelector('#user').addEventListener('click', () => load_user_profile(current_user));

    load_all_posts();
});


function load_all_posts() {
    console.log('All Posts');
    document.querySelector('#all-posts').innerHTML = '<div class="card"> <form id="post-form"> <textarea class="form-control" id="post-body" placeholder="What is on your mind?"></textarea> <input class="btn btn-primary" id="post-button" type="submit" value="Post" style="margin-top: 10px;"></form></div>';
    document.querySelector('#all-posts').style.display = 'block';
    document.querySelector('#following-posts').style.display = 'none';
    document.querySelector('#user-profile').style.display = 'none';

    document.querySelector('#post-button').addEventListener('click', () => {
        if (document.querySelector('#post-body').value == '') {
            alert("Post can't be empty");

        } else {
            post(document.querySelector('#post-body').value);
        }
    })

    fetch(`/api/posts/1/null`)
    .then(response => response.json())
    .then(pages => {
        load_page(pages, 1, '#all-posts', '<div class="card"> <form id="post-form"> <textarea class="form-control" id="post-body" placeholder="What is on your mind?"></textarea> <input class="btn btn-primary" id="post-button" type="submit" value="Post" style="margin-top: 10px;"></form></div>');        
    })
}


function load_following_posts() {
    document.querySelector("#previous-page").disabled = true;
    document.querySelector("#next-page").disabled = true;
    console.log('Following Posts');
    document.querySelector('#all-posts').innerHTML = '<div class="card"> <form id="post-form"> <textarea class="form-control" id="post-body" placeholder="What is on your mind?"></textarea> <input class="btn btn-primary" id="post-button" type="submit" value="Post" style="margin-top: 10px;"></form></div>';
    document.querySelector('#all-posts').style.display = 'none';
    document.querySelector('#following-posts').style.display = 'block';
    document.querySelector('#user-profile').style.display = 'none';

    fetch(`/api/posts/0/null`)
    .then(response => response.json())
    .then(pages => {
        if (pages.message) {
            document.querySelector('#following-posts').innerHTML = '<h2 style="margin-left:10px;">' + pages.message + "</h2>"
        } else {
            console.log(pages);
            document.querySelector('#following-posts').innerHTML = '<h2 style="margin-left:10px;">' + "Posts of people you follow:" + "</h2>";
            load_page(pages, 1, '#following-posts', '<h2 style="margin-left:10px;">' + "Posts of people you follow:" + "</h2>");        
        }
    })
}


function load_user_profile(username) {
    console.log('User Profile');
    document.querySelector('#all-posts').innerHTML = '<div class="card"> <form id="post-form"> <textarea class="form-control" id="post-body" placeholder="What is on your mind?"></textarea> <input class="btn btn-primary" id="post-button" type="submit" value="Post" style="margin-top: 10px;"></form></div>';
    document.querySelector('#all-posts').style.display = 'none';
    document.querySelector('#following-posts').style.display = 'none';
    document.querySelector('#user-profile').innerHTML = '';
    document.querySelector('#user-profile').style.display = 'block';

    fetch(`/api/profiles/${username}`)
    .then(response => response.json())
    .then(user => {
        console.log(user);
        let container = document.createElement('div');
        container.className = 'container';

        let row = document.createElement('div');
        row.className = 'row';

        let username_col = document.createElement('div');
        username_col.className = 'col';
        username_col.innerHTML = '<h1>' + user.username + '</h1>';

        let followers_col = document.createElement('div');
        followers_col.className = 'col';
        followers_col.innerHTML = '<h2>' + user.followers + '</h2>' + '<span class="badge bg-info text-light">' + 'Followers   </span>';

        let following_col = document.createElement('div');
        following_col.className = 'col';
        following_col.innerHTML = '<h2>' + user.following + '</h2>' + '<span class="badge bg-info text-light">' + 'Following   </span>';

        let button_col = document.createElement('div');
        button_col.className = 'col';

        let current_username = document.querySelector('#user').dataset.username;

        if(current_username.localeCompare(username) !== 0) {
            fetch(`/api/is_following/${current_username}/${username}`)
            .then(response => response.json())
            .then(result => {
                console.log(result.is_following);
                let follow_button = document.createElement('button');
                follow_button.className = "btn btn-outline-info";
                follow_button.innerHTML = "Follow";
                follow_button.setAttribute("data-bs-toggle", "button");
                follow_button.type = "button";
                follow_button.style = "margin: 5px;";
                if (result.is_following == true) {
                    follow_button.innerHTML = "Following";
                    follow_button.className = "btn btn-outline-info active";
                    follow_button.setAttribute("aria-pressed", "true");
                }
                follow_button.addEventListener('click', () => follow_toggle(result.is_following, current_username, username));
                button_col.append(follow_button);
            });
        }

        row.append(username_col);
        row.append(followers_col);
        row.append(following_col);
        row.append(button_col);
        container.append(row);
        document.querySelector('#user-profile').append(container);
        
        fetch(`/api/posts/2/${username}`)
        .then(response => response.json()) 
        .then(pages => {
            load_page(pages, 1, '#user-profile', document.querySelector('#user-profile').innerHTML);      
        })
    });
}


function post(bod) {
    fetch('/api/compose', {
        method: 'POST',
        body: JSON.stringify({
            body: bod
        })
    })
    .then(result => {
            console.log(result);
    });
}


function create_post_card(post, div_id) {
    let newPost = document.createElement('div');
    newPost.className = 'card';
    
    let newPostBody = document.createElement('div');
    newPostBody.className = 'card-body';

    let newPostTitle = document.createElement('h5');
    newPostTitle.className = 'card-title post-heading';
    newPostTitle.innerHTML = post.user;
    newPostTitle.addEventListener('click', () => load_user_profile(post.user));
    newPostBody.append(newPostTitle);

    let newPostContent = document.createElement('p');
    newPostContent.className = 'card-text';
    newPostContent.setAttribute('id', `body_${post.id}`)
    newPostContent.innerHTML = post.body;

    // Footer stuff:
    let container = document.createElement('div');
    container.className = 'container px-0 ml-3';

    let footer = document.createElement('div');
    footer.className = 'row no-gutters';

    let date_col = document.createElement('div');
    date_col.className = 'col-sm-2 px-0';

    let date = document.createElement('p');
    date.className = 'card-text';
    date.innerHTML = '<small class="text-muted">' + post.created + '</small>';
    date_col.append(date);

    let like_button_col = document.createElement('div');
    like_button_col.className = 'col-sm-1';

    let edit_button_col = document.createElement('div');
    edit_button_col.className = 'col-sm-1'

    let edit_button = document.createElement('button');
    edit_button.innerHTML = 'Edit';

    let save_button = document.createElement('button');
    save_button.innerHTML = 'Save';

    let edit_text = document.createElement('textarea');
    edit_text.className = 'form-control';
    edit_text.style.display = 'none';
    newPostBody.append(edit_text);

    edit_text.addEventListener('keyup', () => {
        if (edit_text.value == '') {
            save_button.disabled = true;
        } else {
            save_button.disabled = false;
        }
    })

    // Edit Button Logic:
    edit_button.addEventListener('click', () => {
        save_button.style.display = 'block';
        edit_text.style.display = 'block';
        edit_button.style.display = 'none';
        newPostContent.style.display = 'none';
        edit_button_col.append(save_button);

        edit_text.value = newPostContent.innerHTML;

        save_button.addEventListener('click', () => {
            newPostContent.innerHTML = edit_text.value;
            save_button.style.display = 'none';
            edit_text.style.display = 'none';
            newPostContent.style.display = 'block';
            edit_button.style.display = 'block';

            save_changes(post.id, edit_text.value)
        })
    })
    edit_button_col.append(edit_button);

    // Like Button Logic:
    let current_username = document.querySelector('#user').dataset.username;
    fetch(`/api/likes/${current_username}/${post.id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result.is_liked);
        let like_button = document.createElement('button');
        like_button.setAttribute('id', `like_button_${post.id}`)
        like_button.className = "btn btn-outline-danger float-right";
        like_button.innerHTML = "Like";
        like_button.setAttribute("data-bs-toggle", "button");
        like_button.type = "button";
        if (result.is_liked == true) {
            like_button.innerHTML = "Liked";
            like_button.className = "btn btn-outline-danger active";
            like_button.setAttribute("aria-pressed", "true");
        }
        like_button.addEventListener('click', () => like_toggle(current_username, post.id));
        like_button_col.append(like_button);
    });
    
    let likes_col = document.createElement('div');
    likes_col.className = 'col-sm-1 ml-2';

    let likes = document.createElement('h5');
    likes.innerHTML = post.likes;
    likes.setAttribute('id', `likes_${post.id}`)
    likes_col.append(likes);

    footer.append(date_col);
    footer.append(like_button_col);
    footer.append(likes_col);
    if (current_username.localeCompare(post.user) === 0) {
        footer.append(edit_button_col)
    }
    container.append(footer);
    newPostBody.append(newPostContent);
    newPost.append(newPostBody);
    newPost.append(container);

    document.querySelector(div_id).append(newPost);
}


function follow_toggle(state, current_username, username) {
    fetch(`/api/is_following/${current_username}/${username}`, {
        method: 'PUT',
        body: JSON.stringify({
            following: state
        })
    })
    setTimeout(function() {
        load_user_profile(username);
    }, 200);
}


function like_toggle(current_username, post_id) {
    fetch(`/api/likes/${current_username}/${post_id}`)
    .then(response => response.json())
    .then(result => {
        let state = result.is_liked;
        var val = parseInt(document.querySelector(`#likes_${post_id}`).innerHTML);
        if (state) {
            document.querySelector(`#likes_${post_id}`).innerHTML = val - 1;
            document.querySelector(`#like_button_${post_id}`).className = "btn btn-outline-danger float-right";
            document.querySelector(`#like_button_${post_id}`).innerHTML = "Like";
            document.querySelector(`#like_button_${post_id}`).setAttribute("data-bs-toggle", "button");
        } else {
            document.querySelector(`#likes_${post_id}`).innerHTML = val + 1;
            document.querySelector(`#like_button_${post_id}`).className = "btn btn-outline-danger active";
            document.querySelector(`#like_button_${post_id}`).innerHTML = "Liked";
            document.querySelector(`#like_button_${post_id}`).setAttribute("aria-pressed", "true");
        }

        fetch(`/api/likes/${current_username}/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                liked: state
            })
        })
    })
}


function save_changes(post_id, edits) {
    fetch(`/api/post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: edits
        })
    })
}


function load_page(pages, current_page_index, div_id, reset) {
    if (current_page_index !== 1) {
        document.querySelector(div_id).innerHTML = '';
    }
    current_page = pages[current_page_index];
    console.log(current_page);

    current_page.posts.forEach(post => {
        create_post_card(post, div_id);
    });
    
    if (current_page.has_previous === false) {
        document.querySelector("#previous-page").disabled = true;
    } else {
        document.querySelector("#previous-page").disabled = false;
        document.querySelector("#previous-page").onclick = () => {
            current_page_index = current_page_index - 1;
            if (current_page_index === 1) {
                document.querySelector(div_id).innerHTML = reset; 
            } 
            load_page(pages, current_page_index, div_id, reset);
        }
    }

    if (current_page.has_next === false) {
        document.querySelector("#next-page").disabled = true;
    } else {
        document.querySelector("#next-page").disabled = false;
        document.querySelector("#next-page").onclick = () => {
            current_page_index = current_page_index + 1;
            load_page(pages, current_page_index, div_id, reset);
        }
    }
}

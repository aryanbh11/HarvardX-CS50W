document.addEventListener('DOMContentLoaded', function() {

    // Navigation Buttons
    document.querySelector('#all').addEventListener('click', load_all_posts);

    load_all_posts();
});


function load_all_posts() {
    console.log('All Posts');
    document.querySelector('#all-posts').style.display = 'block';

    fetch(`/api/posts/1/null`)
    .then(response => response.json())
    .then(pages => {
        load_page(pages, 1, '#all-posts', '');        
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
    
    let likes_col = document.createElement('div');
    likes_col.className = 'col-sm-1 ml-2';

    let likes = document.createElement('h5');
    likes.innerHTML = "Likes: " + post.likes;
    likes.setAttribute('id', `likes_${post.id}`)
    likes_col.append(likes);

    footer.append(date_col);
    footer.append(likes_col);
    container.append(footer);
    newPostBody.append(newPostContent);
    newPost.append(newPostBody);
    newPost.append(container);

    document.querySelector(div_id).append(newPost);
}

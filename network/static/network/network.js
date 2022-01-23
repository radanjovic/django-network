// Creating event listeners for buttons for editing posts
// This part of code is made thanks to little help from mplungjan from StackOverflow
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#post_container').addEventListener('click', function(e) {
        const tgt = e.target.closest('.edit_post_button');
        if (tgt) {
            const postDiv = tgt.closest('.post_div');
            postDiv.querySelector('.post').style.display = 'none';
            postDiv.querySelector('.edit_post').style.display = 'block';
        }
    });
});


// Creating event listeners for Save buttons on edited post, and sending it
// via API to db, then updating the page to display the updated post
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#post_container').addEventListener('click', function(e) {
        const tgt = e.target.closest('.save_edit_post_button');
        if (tgt) {
            const postDiv = tgt.closest('.post_div');
            const content = postDiv.querySelector('.edited_content').value;
            const id = postDiv.querySelector('.post_id').value; 
            fetch(`/edit/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  content: `${content}`
                })
              }).then (function() {
                    postDiv.querySelector('.post_content').innerHTML = `${content}`;
                    postDiv.querySelector('.post').style.display = 'block';
                    postDiv.querySelector('.edit_post').style.display = 'none';
              });
        }
    });
});


// Checking if there is an Unlike button from our template and showing it
// if there is, else showing Like button.
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like_container').forEach(like => {
        const already_liked = like.querySelector('.already_liked');
        if (already_liked) {
            like.querySelector('.unlike_view').style.display = 'block';
        } else {
            like.querySelector('.like_view').style.display = 'block';
        }
    });
});


// Creating EL for Like button and updating Likes if Like button is clicked.
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#post_container').addEventListener('click', function(e) {
        const tgt = e.target.closest('.like_button');
        if (tgt) {
            const likeDiv = tgt.closest('.like_container');
            const id = likeDiv.querySelector('.post_id_2').value;
            let like_count = likeDiv.querySelector('.like_count').innerHTML;
            like_count++;
            fetch(`/like/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  action: 'like',
                  like_count: `${like_count}`
                })
              }).then (function() {
                    likeDiv.querySelector('.like_count').innerHTML = `${like_count}`;
                    likeDiv.querySelector('.unlike_view').style.display = 'block';
                    likeDiv.querySelector('.like_view').style.display = 'none';
              });
        }
    });
});


// Creating EL for Unlike button and updating Likes if Unlike button is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#post_container').addEventListener('click', function(e) {
        const tgt = e.target.closest('.unlike_button');
        if (tgt) {
            const likeDiv = tgt.closest('.like_container');
            const id = likeDiv.querySelector('.post_id_2').value;
            let like_count = likeDiv.querySelector('.like_count').innerHTML;
            like_count--;
            fetch(`/like/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                  action: 'unlike',
                  like_count: `${like_count}`
                })
              }).then (function() {
                    likeDiv.querySelector('.like_count').innerHTML = `${like_count}`;
                    likeDiv.querySelector('.unlike_view').style.display = 'none';
                    likeDiv.querySelector('.like_view').style.display = 'block';
              });
        }
    });
});
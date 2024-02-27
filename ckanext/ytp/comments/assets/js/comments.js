function ShowCommentForm(id){
    $("#" + id).removeClass('d-none');
}

function editComment(id) {
    document.querySelector(`#comment-${id}`).classList.add('d-none');
    document.querySelector(`#edit-${id}`).classList.remove('d-none');
}

function cancelEditComment(id) {
    document.querySelector(`#comment-${id}`).classList.remove('d-none');
    document.querySelector(`#edit-${id}`).classList.add('d-none');
}


function replyComment(id) {
    cancelEditComment(id);
    document.querySelector(`#reply-${id}`).classList.remove('d-none');
}

function cancelReplyComment(id) {
    document.querySelector(`#reply-${id}`).classList.add('d-none');
}

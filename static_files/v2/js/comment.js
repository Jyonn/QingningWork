function review_switcher_change(like) {
    var review_switcher = $('#review-switcher');
    review_switcher.prop('checked', like);
}

$(document).ready(function () {
    var review_switcher = $('#review-switcher');
    switcher_state_changer(
        review_switcher,
        $('#review-state'),
        '通过作品',
        '驳回作品（没有通过审核）',
        'hint-success',
        'hint-danger',
    );

    var comment_do = $('#comment-do'),
        comment_content = $('.comment-content');
    comment_do.on('click', function () {
        var pass = (review_switcher === undefined) ? false : review_switcher.is(':checked');
        var post = {
            content: comment_content.val(),
            pass: pass,
            event_id: comment_do.attr('data-event'),
            work_id: comment_do.attr('data-work'),
            owner_id: comment_do.attr('data-owner'),
        },
            json = encodedJSON(post);
        hide_comment_box();
        postJSON('/api/work/comment', json, function (response) {
            if (response.code !== 0) {
                show_hint(response.msg)
            }
            else {
                show_hint('评论成功', 500, function () {
                    window.location.reload()
                });
            }
        })
    });
});

function delete_comment(o_delete) {
    alert('确认删除评论？', 'delete-comment', function () {
        var comment_id = $(o_delete).attr('data-comment-id'),
            work_id = $(o_delete).attr('data-work-id'),
            post = {
                comment_id: comment_id,
                work_id: work_id,
            },
            json = encodedJSON(post);
        postJSON('/api/work/comment/delete', json, function (response) {
            if (response.code === 0)
                window.location.reload();
            else
                show_hint(response.msg)
        });
    }, null);
}
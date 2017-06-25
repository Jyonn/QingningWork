function review_switcher_change(like) {
    let review_switcher = $('#review-switcher');
    review_switcher.prop('checked', like);
}

$(document).ready(function () {
    let review_switcher = $('#review-switcher');
    switcher_state_changer(
        review_switcher,
        $('#review-state'),
        '通过作品',
        '驳回作品（没有通过审核）',
        'hint-success',
        'hint-danger',
    );

    let comment_do = $('#comment-do'),
        comment_content = $('.comment-content'),
        comment_container = $('.comment-container');
    comment_do.on('click', function () {
        let pass = (review_switcher === undefined) ? false : review_switcher.is(':checked');
        let post = {
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
                let old_html_id = response.body.old_html_id,
                    new_html_id = response.body.new_html_id,
                    old_html = $(`#${old_html_id}`);
                comment_container.prepend(response.body.new_html);
                if (old_html_id === null) {
                    let new_html = $(`#${new_html_id}`);
                    new_html.slideDown()
                }
                else {
                    old_html.slideUp('250', function () {
                        old_html.remove();
                        let new_html = $(`#${new_html_id}`);
                        new_html.slideDown()
                    })
                }
            }
        })
    });
});

function delete_comment(raw_o_delete) {
    alert('确认删除评论？', 'delete-comment', function () {
        let o_delete = $(raw_o_delete),
            o_comment = o_delete.parent(),
            comment_id = o_delete.attr('data-comment-id'),
            work_id = o_delete.attr('data-work-id'),
            post = {
                comment_id: comment_id,
                work_id: work_id,
            },
            json = encodedJSON(post);
        postJSON('/api/work/comment/delete', json, function (response) {
            if (response.code === 0) {
                o_comment.slideUp('250', function () {
                    o_comment.remove()
                })
            }
            else
                show_hint(response.msg)
        });
    }, null);
}

$(document).ready(function () {
    $('.comment').slideDown()
});
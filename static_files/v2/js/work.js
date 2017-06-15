/**
 * Created by adelliu on 2017/4/18.
 */

function resize() {
    $('.preview-content').each(function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + 'px';
        if (this.style.height !== this.scrollHeight + 'px') {
            this.style.height = this.scrollHeight + 'px';
        }
    }).on('input', function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + 'px';
    });
}

$(document).ready(function () {
    resize();
    window.onresize = resize;

    var comment_btn = $('#comment-btn'),
        comment_box = $('.comment-box'),
        comment_content = $('.comment-content'),
        comment_cancel = $('#comment-cancel'),
        comment_mask = $('#comment-mask');
    comment_btn.on('click', function () {
        comment_box.animate({bottom: '0'}, function () {
            comment_mask.css('display', 'inherit');
        });
        comment_content.focus();
    });
    comment_cancel.on('click', hide_comment_box);
    comment_mask.on('click', hide_comment_box);

    var create_work = $('#create-work'),
        work_edit_work_name_input = $('#work-edit-work-name-input'),
        work_edit_writer_name_input = $('#work-edit-writer-name-input'),
        work_edit_work_content = $('#work-edit-work-content'),
        switch_for_public = $('#switch-for-public');
    create_work.on('click', function () {
        var post = {
            work_name: work_edit_work_name_input.val(),
            writer_name: work_edit_writer_name_input.val(),
            content: work_edit_work_content.val(),
            is_public: switch_for_public.length === 0 || switch_for_public.is(':checked'),
        },
            json = encodedJSON(post);
        if (post.work_name === '') {
            show_hint('作品名不允许为空');
            return;
        }
        if (post.writer_name === '') {
            show_hint('作者名不允许为空');
            return;
        }
        if (post.content === '') {
            show_hint('正文不允许为空');
            return;
        }
        postJSON('/work/upload', json, function (response) {
            if (response.code === 0) {
                show_hint('发布成功', 500, function () {
                    window.location.href = response.body
                });
            }
            else {
                show_hint(response.msg)
            }
        })
    })
});

function do_thumb(thumb_btn_raw) {
    var thumb_btn = $(thumb_btn_raw);
    var thumb_icon = thumb_btn.children('i'),
        like = thumb_icon.hasClass('fa-thumbs-o-up');
    var post = {
        event_id: thumb_btn.attr('data-event'),
        work_id: thumb_btn.attr('data-work'),
        owner_id: thumb_btn.attr('data-owner'),
        like: like,
    },
        json = encodedJSON(post);
    postJSON('/work/like', json, function (response) {
        var event_item = thumb_btn.parent().parent(),
            me_thumb = event_item.find('#me-thumb'),
            text_desc = event_item.find('#text-desc-thumb'),
            thumb_count = parseInt(text_desc.attr('data-thumb'));
        if (response.code === 0) {
            if (like) {
                thumb_count += 1;
                me_thumb.css('display', 'inline');
                thumb_icon.removeClass('fa-thumbs-o-up').addClass('fa-thumbs-up');
            }
            else {
                thumb_count -= 1;
                me_thumb.css('display', 'none');
                thumb_icon.removeClass('fa-thumbs-up').addClass('fa-thumbs-o-up');
            }
            if (thumb_count === 0)
                text_desc.text('成为第一个赞的人吧');
            else
                text_desc.text('等'+thumb_count+'人觉得赞');
            text_desc.attr('data-thumb', thumb_count);
            review_switcher_change(like);
        }
        else {
            show_hint(response.msg)
        }
    });
}

function hide_comment_box() {
    var comment_box = $('.comment-box'),
        comment_mask = $('#comment-mask');
    comment_mask.css('display', 'none');
    comment_box.animate({bottom: '-180px'});
}
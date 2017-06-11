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
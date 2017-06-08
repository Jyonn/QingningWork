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

function hide_comment_box() {
    var comment_box = $('.comment-box'),
        comment_mask = $('#comment-mask');
    comment_mask.css('display', 'none');
    comment_box.animate({bottom: '-180px'});
}
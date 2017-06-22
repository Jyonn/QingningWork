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
        modify_work = $('#modify-work'),
        work_edit_work_name_input = $('#work-edit-work-name-input'),
        work_edit_writer_name_input = $('#work-edit-writer-name-input'),
        work_edit_work_content = $('#work-edit-work-content'),
        switch_for_public = $('#switch-for-public'),
        work_edit_motion = $('#work-edit-motion');

    switcher_state_changer(
        switch_for_public,
        $('#switch-public-desc'),
        '所有人可以看',
        '仅我可见',
        'hint-normal',
        'hint-normal'
    );

    function finish_work(type, work_id) {
        var post = {
            work_name: work_edit_work_name_input.val(),
            writer_name: work_edit_writer_name_input.val(),
            content: work_edit_work_content.val(),
            motion: work_edit_motion.val(),
            is_public: switch_for_public.length === 0 || switch_for_public.is(':checked'),
        };
        if (work_id !== null)
            post.work_id = work_id;
        var json = encodedJSON(post);
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
        postJSON('/api/work/'+type, json, function (response) {
            if (response.code === 0) {
                show_hint('发布成功', 500, function () {
                    window.location.href = '/v2/event/' + response.body.owner_id + '/' +
                        response.body.work_id + '/' + response.body.event_id
                });
            }
            else {
                show_hint(response.msg)
            }
        })
    }

    create_work.on('click', function () { finish_work('upload', null)} );
    modify_work.on('click', function () { finish_work('modify', modify_work.attr('data-work'))} );
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
    postJSON('/api/work/like', json, function (response) {
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

$(document).ready(function () {
    var event_menu_container = $('#event-menu-container'),
        event_id = event_menu_container.attr('data-event'),
        work_id = event_menu_container.attr('data-work'),
        owner_id = event_menu_container.attr('data-owner');
    var item_share = $('#item-share'),
        item_private = $('#item-private'),
        item_modify = $('#item-modify'),
        item_delete = $('#item-delete');
    item_delete.on('click', function () {
        alert('不可撤销，确认删除文章？', 'delete-work', function () {
            var post = {
                event_id: event_id,
                work_id: work_id,
                owner_id: owner_id,
            },
                json = encodedJSON(post);
            postJSON('/api/work/delete', json, function (response) {
                if (response.code === 0) {
                    window.location.href = '/v2/center'
                }
                else {
                    show_hint(response.msg)
                }
            })
        }, null);
    });
    item_modify.on('click', function () {
        alert('修改后数据清零，是否确认修改？', 'modify-work', function () {
            window.location.href = '/v2/work/modify/'+work_id
        }, null);
    })
});
/**
 * Created by Adel on 2017/6/2.
 */

$(document).ready(function () {
    var nav_user_avatar = $('#nav-user-avatar'),
        sidebar = $('.sidebar-container'),
        sidebar_fold_btn = $('#sidebar-fold-btn'),
        sidebar_mask = $('#sidebar-mask');

    nav_user_avatar.on('click', function () {
        nav_user_avatar.stop().animate({right: '-40px'}, function () {
            sidebar.stop().animate({right: '0'}, function () {
                sidebar_mask.css('display', 'inherit');
            });
        });
    });
    sidebar_fold_btn.on('click', function () {
        sidebar_mask.css('display', 'none');
        sidebar.stop().animate({right: '-200px'}, function () {
            nav_user_avatar.stop().animate({right: '0'});
        });
    });
    sidebar_mask.on('click', function () {
        sidebar_mask.css('display', 'none');
        sidebar.stop().animate({right: '-200px'}, function () {
            nav_user_avatar.stop().animate({right: '0'});
        });
    });
});
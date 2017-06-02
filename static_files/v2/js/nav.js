/**
 * Created by Adel on 2017/6/2.
 */

$(document).ready(function () {
    var nav_user_avatar = $('#nav-user-avatar'),
        sidebar = $('.sidebar-container'),
        sidebar_fold_btn = $('#sidebar-fold-btn');
    nav_user_avatar.on('click', function () {
        nav_user_avatar.animate({right: '-40px'}, function () {
            sidebar.animate({right: '0'});
        });
    });
    sidebar_fold_btn.on('click', function () {
        sidebar.animate({right: '-200px'}, function () {
            nav_user_avatar.animate({right: '0'});
        });
    })
});
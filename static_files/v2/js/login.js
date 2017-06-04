var ACT_LOGIN = 0,
    ACT_SIGNUP = 1,
    ACT_UNKNOWN = 2;

$(document).ready(function() {
    var login_act = $('#login-act'),
        signup_act = $('#signup-act'),
        current_act = ACT_LOGIN;
    login_act.on("click", function () {
        if (current_act === ACT_SIGNUP) {
            current_act = ACT_UNKNOWN;
            login_act.stop().animate({'top': '0'});
            signup_act.stop().animate({'top': '60px'});
            login_act.removeClass('btn-white').addClass('btn-green');
            signup_act.removeClass('btn-green').addClass('btn-white');
            current_act = ACT_LOGIN;
        }
        else if (current_act === ACT_LOGIN) {

        }
    });
    signup_act.on('click', function () {
        if (current_act === ACT_LOGIN) {
            current_act = ACT_UNKNOWN;
            signup_act.stop().animate({'top': '0'});
            login_act.stop().animate({'top': '60px'});
            signup_act.removeClass('btn-white').addClass('btn-green');
            login_act.removeClass('btn-green').addClass('btn-white');
            current_act = ACT_SIGNUP;
        }
        else if (current_act === ACT_SIGNUP) {

        }
    });

    var captcha = $('.captcha');
    captcha.on('click', function () {
        captcha.attr('src', '/base/captcha/img/');
    });
});

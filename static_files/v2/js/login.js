var ACT_LOGIN = 0,
    ACT_SIGNUP = 1;

function refresh_captcha_img(captcha) {
    captcha.attr('src', '/base/captcha/img');
}

$(document).ready(function() {
    var login_act = $('#login-act'),
        signup_act = $('#signup-act'),
        current_act = ACT_LOGIN;
    var username_input = $('#username-input'),
        password_input = $('#password-input'),
        captcha_input = $('#captcha-input');
    var captcha = $('.captcha');
    login_act.on("click", function () {
        if (current_act === ACT_SIGNUP) {
            login_act.stop().animate({'top': '0'});
            signup_act.stop().animate({'top': '60px'});
            login_act.removeClass('btn-white').addClass('btn-green');
            signup_act.removeClass('btn-green').addClass('btn-white');
            current_act = ACT_LOGIN;
        }
        else if (current_act === ACT_LOGIN) {
            var post = {
                username: username_input.val(),
                password: password_input.val(),
                captcha: captcha_input.val(),
            },
                json = encodedJSON(post);
            postJSON('/api/user/login', json, function (response) {
                refresh_captcha_img(captcha);
                if (response.code !== 0)
                    show_hint(response.msg);
                else {
                    show_hint('登录成功');
                    window.location.href = '/v2/center'
                }
            });
        }
    });
    signup_act.on('click', function () {
        if (current_act === ACT_LOGIN) {
            signup_act.stop().animate({'top': '0'});
            login_act.stop().animate({'top': '60px'});
            signup_act.removeClass('btn-white').addClass('btn-green');
            login_act.removeClass('btn-green').addClass('btn-white');
            current_act = ACT_SIGNUP;
        }
        else if (current_act === ACT_SIGNUP) {
            var post = {
                username: username_input.val(),
                password: password_input.val(),
                captcha: captcha_input.val(),
            },
                json = encodedJSON(post);
            postJSON('/api/user/register', json, function (response) {
                refresh_captcha_img(captcha);
                if (response.code !== 0)
                    show_hint(response.msg);
                else {
                    show_hint('注册成功');
                    window.location.href = '/v2/center'
                }
            });
        }
    });

    captcha.on('click', function () {
        refresh_captcha_img();
    });
});

var is_hinting = false;

function show_hint(text, last_time=500) {
    if (is_hinting)
        return;
    is_hinting = true;
    var hint_body = $('.hint-body'),
        hint_box = $('.hint-box');
    hint_body.text(text);
    hint_box.fadeIn('250');
    setTimeout(function () {
        hint_box.fadeOut('250')
        is_hinting = false;
    }, last_time);
}
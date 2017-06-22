function alert(text, id_str, success_func, cancel_func) {
    var rand_str;
    if (id_str === "")
        rand_str = Math.random().toString(36).substr(2);
    else
        rand_str = id_str;
    var alert_box = "alert-box-" + rand_str,
        alert_ok = "alert-ok-" + rand_str,
        alert_cancel = "alert-cancel-" + rand_str,
        alert_mask = "alert-mask-" + rand_str,
        mask_html = '<div class="body-mask press" id="'+alert_mask+'"></div>',
        alert_html =
        '<div class="alert-box" id="'+alert_box+'" style="display: none;">' +
        '   <div class="alert-body">'+text+'</div>' +
        '   <hr>' +
        '   <div class="alert-btns">' +
        '       <div class="alert-btn press alert-ok" id="'+alert_ok+'">确定</div>' +
        '       <div class="alert-btn press alert-cancel" id="'+alert_cancel+'">取消</div>' +
        '   </div>' +
        '</div>';
    $('body').append(mask_html).append(alert_html);
    var j_alert_mask = $('#'+alert_mask),
        j_alert_ok = $('#'+alert_ok),
        j_alert_cancel = $('#'+alert_cancel),
        j_alert_box = $('#'+alert_box);
    j_alert_mask.fadeIn('250');
    j_alert_box.fadeIn('250');
    function disappear() {
        j_alert_mask.fadeOut('250', function () {
            j_alert_mask.remove();
        });
        j_alert_box.fadeOut('250', function () {
            j_alert_box.remove();
        });
    }
    j_alert_mask.on('click', function () {
        disappear();
        if (cancel_func !== null)
            cancel_func();
    });
    j_alert_ok.on('click', function () {
        disappear();
        if (success_func !== null)
            success_func();
    });
    j_alert_cancel.on('click', function () {
        disappear();
        if (cancel_func !== null)
            cancel_func();
    });
}
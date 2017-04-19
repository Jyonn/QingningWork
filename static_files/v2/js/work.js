/**
 * Created by adelliu on 2017/4/18.
 */

function resize_content(content) {

}

$(document).ready(function () {
    $('#work-content').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;');
    }).on('input', function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + 'px';
    });
});
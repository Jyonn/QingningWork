/**
 * Created by adelliu on 2017/4/18.
 */

function resize() {
    $('.preview-content').each(function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + 'px';
        alert(this.style.height);
        alert(this.scrollHeight);
    }).on('input', function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + 'px';
    });
}

$(document).ready(function () {
    resize();
    window.onresize = resize;
});
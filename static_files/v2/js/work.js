/**
 * Created by adelliu on 2017/4/18.
 */

function resize_content(content) {

}

$(document).ready(function () {
    // console.log($('.preview-content').length);
    alert(">>>");
    $('.preview-content').each(function () {
        this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;');
    }).on('input', function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + 'px';
    });
});
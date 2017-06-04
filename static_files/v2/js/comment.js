$(document).ready(function () {
    var review_switcher = $('#review-switcher'),
        review_state = $('#review-state');
    review_switcher.on('change', function () {
        var checked = review_switcher.prop('checked');
        if (checked) {
            review_state.text('通过作品').removeClass('hint-danger').addClass('hint-success');
        }
        else {
            review_state.text('驳回作品（没有通过审核）').removeClass('hint-success').addClass('hint-danger');
        }
    });
});
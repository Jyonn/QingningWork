function postForm(url, form_data, success_function, error_function=null) {
    $.ajax({
        url : url,
        type : 'POST',
        data : form_data,
        processData : false,
        async: true,
        dataType : '',
        contentType : false,
        success : success_function,
        error : error_function,
    });
}

function postJSON(url, json_str, success_function, error_function=null) {
    $.ajax({
        url : url,
        type : 'POST',
        data : json_str,
        async: true,
        dataType : 'json',
        contentType : 'application/text',
        success : success_function,
        error: error_function,
    });
}

function encodedJSON(dict) {
    for (let key in dict)
        if (dict.hasOwnProperty(key)) {
            dict[key] = Base64.encode(dict[key]);
        }
    return $.toJSON(dict)
}

function switcher_state_changer(switcher, text_holder, on_text, off_text, on_class, off_class) {
    switcher.on('change', function () {
        if (switcher.is(':checked'))
            text_holder.text(on_text).removeClass(off_class).addClass(on_class);
        else
            text_holder.text(off_text).removeClass(on_class).addClass(off_class);
    })
}

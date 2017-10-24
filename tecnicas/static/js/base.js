// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function imprimir_mensaje(selector, mensaje, tipo) {
    var html = '<div class="alert alert-' + tipo + '">' + mensaje + '<button type="button" class="close" data-dismiss="alert">x</button></div>';
    $(selector).html(html);
}

$(document).ready(function () {
    $('.expand').on('click', function (evt) {
        evt.preventDefault();
        $el = $(this);
        var id = $el.data("id");
        var opn = $el.data("open");
        if (opn == '0') {
            $el.data("open", "1");
            $el.html("<i class='fa fa-angle-double-up'></i><span>Contraer Comentarios</span>");
            $wcomments = $("#wcomment" + id)
            $wcomments.slideDown(300, function () {
                $wcomments.css("display", "block");
            });
        } else {
            $el.data("open", "0");
            $el.html("<i class='fa fa-angle-double-down'></i><span>Expandir Comentarios</span>");
            $widget = $("#wcomment" + id);
            $data = $("#comments-" + id + " li");
            $widget.slideUp(300, function () {
                $widget.css("display", "none");
            });
        }
    });
});

Object.size = function (obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function report_django_error_input(data, selector) {
    /*
     Function:
     data : forms.errors en formato JSON de un formulario de Django.
     */

    selector = selector || false;
    $form_groups = $('.form-group');
    $form_groups.removeClass('has-error')
        .removeAttr('data-toggle');
    /* Clean all errors */
    $form_groups.find('[data-toggle="tooltip"]')
        .removeAttr('data-toggle')
        .tooltip('destroy');
    for (key in data) {

        $input = $('#id_' + key);
        $input.closest('.form-group').addClass('has-error');
        $input.attr('data-toggle', 'tooltip');
        title = '';
        for (j = 0; j < data[key].length; j++) {
            title += data[key][j] + '\n'
        }
        $input.attr('title', title);
    }
    if (selector) {
        if (data.__all__) {
            $(selector).find('.all').html(
                '<div class="alert alert-danger">' + data.__all__ + '</div>'
            );
        }
    }
    $('[data-toggle="tooltip"]').tooltip();
}

function clean_django_error(form_selector) {
    selector = form_selector || false;
    $form_groups = $('.form-group');
    $form_groups.removeClass('has-error')
        .removeAttr('data-toggle');
    /* Clean all errors */
    $form_groups.find('[data-toggle="tooltip"]')
        .removeAttr('data-toggle')
        .tooltip('destroy');
    if (selector) {

        $(selector).find('.all').html(
            ''
        );
    }
}

function stripHTML(dirtyString) {
	var container = document.createElement('div');
	container.innerHTML = dirtyString;
	return container.textContent
}
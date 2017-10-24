url_edit_comment = null
url_brainstorming_search_form_item = null
url_brainstorming_add_comment_item = null
url_brainstorming_sesionitems = null;
url_moderation = null;

function crear_item(url) {
    //var bandera = $('#form_item').valid();
    var titulo = $('#id_titulo').val();
    var descripcion = $('#id_descripcion').val();
    if (titulo != '') {
        if (descripcion != '') {
            $.post(url, {titulo: titulo, descripcion: descripcion}, function (data) {
                idea = {
                    id: data.id,
                    titulo: titulo,
                    descripcion: descripcion,
                    fecha: moment(data.fecha, "YYYY-MM-DD").format('LL'),
                    url: data.url
                };
                $('#id_titulo').val('');
                $('#id_descripcion').val('');
                imprimir_mensaje('#modal_message', 'Se ha creado su idea con exito', 'info');
                tmpl = swig.compile($("#ideaTemplate").html(), {filename: 'ideaTemplate'});
                $("#ideas_list").prepend(tmpl(idea))
            }).fail(function () {
                imprimir_mensaje('#modal_message', 'No se pueden crear ideas en esta sesión', 'danger');
            });

        } else {
            imprimir_mensaje('#modal_message', 'Debe ingresar una descripción', 'error');
        }
    } else {
        imprimir_mensaje('#modal_message', 'Debe ingresar un titulo', 'error');
    }
}

function search_form_add_comment_item(url, voto, id_item) {
    $.getJSON(url, {voto: voto, id_item: id_item}, function (data) {
        $('#modal_content_commnet').html(data.form);
        $("#idea_titulo").html(data.idea_tit);
        $("#idea_descripcion").html(data.idea_desc);
        $("#id_voto option[value='" + voto + "']").attr("selected", true);
    })
}

function form_add_comment_item(url) {
    $.post(url, $('#id_commnet_form').serialize(), function (data) {
        if (data['error']) {
            imprimir_mensaje('#modal_message_comment', data['mensaje'], 'error');
        } else {
            imprimir_mensaje('#modal_message_comment', data['mensaje'], 'info');
            var comment = {
                comment: $('#id_comment').val(),
                submit_date: moment().format('LLL'),
                vote: $('#id_voto').val(),
                id: data['id_comment']
            };
            var tmplcomment = swig.compile($('#commentTemplate').html(), {filename: 'commentTemplate'});
            var id = $('#id_object_pk').val();
            $('#comments-' + id).prepend(tmplcomment(comment));
            $('#id_email').val('');
            $('#id_comment').val();
            $('#like-' + id).removeAttr('href');
            $('#dislike-' + id).removeAttr('href');
        }
    });
}

$(document).ready(function () {
    var $ideas_list = $('#ideas_list');
    $ideas_list.on('click', '.like', function(){
        var id_item = $(this).attr('id');
        if (id_item) {
            id_item = id_item.split('-')[1];
        }
        if (id_item) {
            search_form_add_comment_item(url_brainstorming_search_form_item, '+', id_item);
        }
    });

    $ideas_list.on('click', '.dislike', function(){
        var id_item = $(this).attr('id');
        if (id_item) {
            id_item = id_item.split('-')[1];
        }

        if (id_item) {
            search_form_add_comment_item(url_brainstorming_search_form_item, '-', id_item);
        }
    });

    $ideas_list.on('click', '.coord',function(){
        var id_item = $(this).attr('id');
        var metodo = "";
        $('#modal_moderation').find('#modal_moderation_message').html('');
        console.log(id_item);
        if (id_item) {
            metodo = id_item.split('-')[0];
            id_item = id_item.split('-')[1];
            $("#item_mod").val(id_item);
            $("#method_mod").val(metodo);
        }
    });

    $('#save_comment_item').on('click', function(){
        form_add_comment_item(url_brainstorming_add_comment_item)
    });

    $('#save_item').on('click', function(){
        crear_item(url_brainstorming_sesionitems);
    });

    $('#save_comment_mod').on('click',function(evt){
        $.post(url_moderation, $("#form_mod").serialize(), function(data){
            if(data.done){
                imprimir_mensaje('#modal_moderation_message', data.message, 'success');
                $("#form_mod").children('input').val('');
                $("#form_mod").children('textarea').val('');
                if(data.reload){
                    setInterval(function(){
                        location.reload();
                    },3000);
                }
            }else{
                imprimir_mensaje('#modal_moderation_message', data.message, 'error');
            }
        }).fail(function(){
                imprimir_mensaje('#modal_moderation_message', 'La idea seleccionada no existe, no se puede moderar', 'danger');
            });


    });
    $('a[data-liked="1"]').addClass('success');
    $('a[data-disliked="1"]').addClass('danger');
});
url_crear_pregunta = '';
url_crear_respuesta = '';
url_eliminar_respuesta = '';
url_eliminar_pregunta = '';

function crear_pregunta(form){
    if($('#id_texto_pregunta').val() != ''){
        $.post(url_crear_pregunta, form.serialize(), function(data){
            var tmp = swig.compile($("#pregunta_template").html(),{filename:'pregunta'});
            var pregunta = {
                pregunta: {
                    id: data[1],
                    tipo: $('#id_tipo').val(),
                    pregunta: $('#id_texto_pregunta').val()
                }
            };
            var html = tmp(pregunta);
            console.log(html);
            $('#id_texto_pregunta').val('')
            $('#preguntas').append(html);
            $.gritter.add({
                    title:'Exito',
                    text: 'Se ha creado tu Pregunta',
                    time: 3000,
                    sticky: false
                });


        });
    }else{
        $.gritter.add({
            title:'Error',
            text: 'Debe escribir una pregunta',
            time: 3000,
            sticky: false
        });
    }
}

function crear_respuesta(form){
    $.post(url_crear_respuesta, form.serialize(), function(data){
        var tipo = data[2];
        var selector = $("#respuesta_"+tipo+"_template");

        var tmp = swig.compile(selector.html(),{filename:'respuesta_'+tipo});
        var respuesta = {
            respuesta: {
                id: data[1],
                respuesta: $('#id_respuesta').val()
            }
        };
        var html = tmp(respuesta);
        $('#id_respuesta').val('')
        $('#respuestas-'+$('#id_pregunta').val()).append(html);

        $.gritter.add({
                title:'Exito',
                text: 'Se ha creado tu respuesta',
                time: 3000,
                sticky: false
            });
    });
}

function eliminar_respuesta(id){
    $.post(url_eliminar_respuesta, {id_respuesta: id}, function(data){
        $('#respuesta-'+id).remove();

        swal("Borrada!", "Se ha eliminado la respuesta.", "success");
        //$.gritter.add({
        //        title:'Exito',
        //        text: 'Se ha eliminado tu respuesta',
        //        time: 3000,
        //        sticky: false
        //    });
    });
}

function eliminar_pregunta(id){
    $.post(url_eliminar_pregunta, {id_pregunta: id}, function(data){
        $('#pregunta-'+id).remove();

        swal("Borrada!", "Se ha eliminado la pregunta.", "success");
    });
}

$(document).ready(function(){
    $('#crear_pregunta').live('click', function(){
        crear_pregunta($('#form_pregunta'));
    });

    $('.crear_respuesta').live('click', function(){
        var id_pregunta = $(this).attr('id').split('-')[1];
        $('#id_pregunta').val(id_pregunta);
    });

    $('#crear_respuesta').live('click', function(){
        crear_respuesta($('#form_respuesta'));
    });

    $('.eliminar_respuesta').live('click', function(evt){
        evt.preventDefault();
        var id_respuesta = $(this).attr('id').split('-')[1];
        swal({
            title: '',
            text:'¿Desea borrar esta respuesta?',
            type:'warning',
            showCancelButton: true,
            cancelButtonText: 'Cancelar'
        }, function(isConfirm){
            if(isConfirm){
                eliminar_respuesta(id_respuesta);
            }
        });
    });

    $('.eliminar_preguntas').live('click', function(evt){
        evt.preventDefault();
        var id_pregunta = $(this).attr('id').split('-')[1];
        swal({
            title: '',
            text:'¿Desea borrar esta pregunta?',
            type:'warning',
            showCancelButton: true,
            cancelButtonText: 'Cancelar'
        }, function(isConfirm){
            if (isConfirm) {
                eliminar_pregunta(id_pregunta);
            }
        });

    });

});

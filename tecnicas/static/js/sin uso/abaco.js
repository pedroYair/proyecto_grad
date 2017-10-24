url_votacion = null;
url_moderation = null;
function votar(url, form, id_item, comment, voto){
    $.post(url, form.serialize(), function(data){
        $.gritter.add({
                title:'Exito',
                text: data.mensaje,
                time: 3000,
                sticky: false
            });
        var $votacion = $("#votacion-"+id_item);
        form.slideUp();
        $votacion.remove();
        tmp = swig.compile($("#new_comment").html(),{filename:'nuevo_comentario'});
        comment = {
                    id: id_item,
                    fecha: moment().format('LLL'),
                    comment:comment,
                    comment_id: data.comment_id,
                    voto_abaco: traducir_comentario(voto)
                  };
        html = tmp(comment);
        console.log(html);
        $('#commentson-'+id_item).prepend(html);


    }).fail(function(){
            $.gritter.add({
                title:'Error',
                text: 'No se ha podido crear un comentario en esta idea',
                time: 3000,
                sticky: false
            });
        });

}

function cambiar_voto(voto, id_item){
    $('#voto-'+id_item).val(voto);
    var $comment = $('#comment-'+id_item);
    if(voto == '1' || voto == '0'){
        $comment.val('');
    }

}

function traducir_comentario(num){
    if(num=='0'){
        return 'black'
    }else if(num=='1'){
        return 'white'
    }else if(num=='2'){
        return 'red'
    }else if(num=='3'){
        return 'lred'
    }else if(num=='4'){
        return 'yellow'
    }else if(num=='5'){
        return 'lgreen'
    }else if(num=='6'){
        return 'green'
    }
}

$(document).ready(function(){
    $(".gen").click(function(evt){
        $(this).parent().find('.voto').removeClass('active-selected');
        var id_item = $(this).attr('id').split('-')[1];
        cambiar_voto($(this).attr('id').split('-')[2], id_item);
        var $comentario = $("#comentario-"+id_item);
        if($comentario.hasClass("hidden")){
            $comentario.slideToggle('normal',function(){
               $comentario.toggleClass("hidden");
           });
        }
        $(this).addClass('active-selected');
    });
    $(".nogen").click(function(evt){
        $(this).parent().find('.voto').removeClass('active-selected');
        var id_item = $(this).attr('id').split('-')[1];
        cambiar_voto($(this).attr('id').split('-')[2], id_item);
        var $comentario = $("#comentario-"+id_item);
        if(!$comentario.hasClass("hidden")){
            $comentario.slideToggle('normal',function(){
                $comentario.toggleClass("hidden");
            });

        }
        $(this).addClass('active-selected');
    });
    $('.btn-votar').live('click', function(evt){

        var id_item = $(this).attr('id').split('-')[1];
        var voto = $('#voto-'+id_item).val();
        var comment = $('#comment-'+id_item).val();
        if(voto != '-1'){
            if(comment != '' || (voto!= '0' || voto!= '1') ){
                votar(url_votacion, $('#form_comments-'+id_item), id_item, comment, voto);

            }else{
                $.gritter.add({
                title:'Error Comentario',
                text: 'Debe introducir un comentario para su voto.',
                time: 3000,
                sticky: false
            });
            }
        }else{
            $.gritter.add({
                title:'Error Voto',
                text: 'Debe seleccionar uno de los colores para el voto',
                time: 3000,
                sticky: false
            });
        }

    });

    $('.open-comments').click(function(evt){
        evt.preventDefault();
       var id = $(this).attr('id').split('-')[1];
       $('#wcomment-'+id).slideToggle('normal',function(){
            $('#wcomment-'+id).toggleClass('hidden');
       });
       if(!$('#wcomment-'+id).hasClass('hidden')){
           $(this).html('<i class="fa fa-comments"> </i> ver comentarios');
       }else{
           $(this).html('<i class="fa fa-comments"> </i> ocultar comentarios');
       }
    });

    $('.coord').live('click',function(){
        var id_item = $(this).attr('id').split('-')[1];
        var metodo = $(this).attr('id').split('-')[0];
        $("#item_mod").val(id_item);
        $("#method_mod").val(metodo);
    });

});
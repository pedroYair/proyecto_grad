id_comment_global = -1
url_edit_comment = null;

function edit_comment(id_comment, voto, comment, url){
    $.post(url, {id_comment: id_comment, vote: voto, comment: comment}, function(data){
        if(! data['error']){
            $.gritter.add({
                title:'Exito',
                text: 'Su comentario ha sido modificado con exito',
                time: 3000,
                sticky: false
            });
            reset_edit_comment_form();
            change_comment(id_comment, voto, comment);
        }

    }).fail(function() {
            $.gritter.add({
                title:'Error',
                text: 'Usted no puede editar este comentario.',
                time: 3000,
                sticky: false
            });
        });
}

function change_comment(id_comment, voto, comment){
    var jq = $('#text_comment-'+id_comment);
    var text_comment = jq.html();
    text_comment = '<blockquote>'+text_comment+'</blockquote>'+comment;
    jq.html(text_comment);
    var jq_comment_voto = $('#comment_voto-'+id_comment);
    if(voto == '+' || voto == '-'){
        jq_comment_voto.removeClass('dislike');
        jq_comment_voto.removeClass('like');
        jq_comment_voto.removeClass('text-danger');
        jq_comment_voto.removeClass('text-success');
    }
    if(voto == '+'){
        jq_comment_voto.addClass('text-success');
        jq_comment_voto.addClass('like');
        jq_comment_voto.html('<i class="fa fa-thumbs-o-up"></i>De Acuerdo');
    }else if(voto == '-'){
        jq_comment_voto.addClass('text-danger');
        jq_comment_voto.addClass('dislike');
        jq_comment_voto.html('<i class="fa fa-thumbs-o-down"></i>En Desacuerdo');
    }else{
        voto = parseInt(voto);
        if(voto >= 0 && voto <=6){
            jq_comment_voto.removeClass('white')
            jq_comment_voto.removeClass('black')
            jq_comment_voto.removeClass('lred')
            jq_comment_voto.removeClass('red')
            jq_comment_voto.removeClass('yellow')
            jq_comment_voto.removeClass('lgreen')
            jq_comment_voto.removeClass('green')
            var t_voto = traducir_voto_abaco(voto);
            jq_comment_voto.addClass(t_voto);
        }
    }

}

function traducir_voto_abaco(num){
    if(num==0){
        return 'black'
    }else if(num==1){
        return 'white'
    }else if(num==2){
        return 'red'
    }else if(num==3){
        return 'lred'
    }else if(num==4){
        return 'yellow'
    }else if(num==5){
        return 'lgreen'
    }else if(num==6){
        return 'green'
    }
    return null;
}


function seleccionar_voto_comment(){
    var like = $('#edit_comment_like.text-success').length;
    if(like != 0){
        return '+';
    }

    var dislike = $('#edit_comment_dislike.text-danger').length;
    if(dislike != 0){
        return '-';
    }

    var voto_abaco = $('#voto-edit').val();
    if(voto_abaco){
        if(voto_abaco != -1){
            return voto_abaco;
        }
    }

    return null;
}


function reset_edit_comment_form(){
    $('#id_edit_comentario').val('');
    $('#edit_comment_dislike').removeClass('text-danger');
    $('#edit_comment_like').removeClass('text-success');

}

$(document).ready(function(){
    $('#edit_comment_like').live('click', function(){
        $('#edit_comment_like').addClass('text-success');
        $('#edit_comment_dislike').removeClass('text-danger');
    });
    $('#edit_comment_dislike').live('click', function(){
        $('#edit_comment_like').removeClass('text-success');
        $('#edit_comment_dislike').addClass('text-danger');
    });

    $('.edit_comment').live('click', function(){
        id_comment_global = $(this).attr('id').split('-')[1];
    });

    $('#save_edit_comment').live('click', function(){
        if(url_edit_comment != null){
            //edit_comment(url_edit_comment)
            var vote = seleccionar_voto_comment();
            var comment = $('#id_edit_comentario').val();
            if(vote != null){
                if(comment != '' || vote == 0 || vote == 1){
                    edit_comment(id_comment_global, vote, comment, url_edit_comment);
                }else{
                    $.gritter.add({
                        title:'Error',
                        text: 'Debe introducir un nuevo comentario',
                        time: 3000,
                        sticky: false
                    });
                }
            }else{
                $.gritter.add({
                        title:'Error',
                        text: 'Debe votar por la idea.',
                        time: 3000,
                        sticky: false
                    });
            }
        }
    });
});


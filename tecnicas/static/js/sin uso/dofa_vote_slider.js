console.log('loading vote DOFA javascript controller....');
var votar_factor_url = null;
$(function(){
    $slides = $('.for_slide');
    $.each($slides,function(index,value){
        var id = $(value).attr('id').split('-')[1];
        $('#id_voto-'+id).parent().append('<div class="row" id="container_voto_'+id+'">' +
        '<label class="col-md-3">Valoración</label>' +
        '<div class="col-md-7 mtop-5">' +
        '<div id="voto_'+id+'">' +
        '</div>' +
        '</div>' +
        '<button class="btn btn-success save_vote" id="save-'+id+'" class="btn btn-success">Guardar</button>' +
        '</div>');
        $slide = $('#voto_'+id);
        $slide.slider({
            min: -5,
            max: 5,
            value: 0,
            animate: true,
            range: "min",
            slide: function( event, ui ) {
                update(ui.value,$(ui.handle).parent(),id)
            }
        });
    });

    $('.save_vote').click(function(evt){
        var id = $(this).attr('id').split('-')[1];
        var valor = $('#voto_'+id).slider('option','value');
        console.log(votar_factor_url.replace('0',id));
        $.post(votar_factor_url.replace('0',id),{
            voto : valor,
            factor: id
        },function(response){
            if(response.creado){
                console.log(response.valor_factor);
                $('#container_voto_'+id).remove();
                var type = (valor > 0) ? 'label-success' : 'label-danger';
                $('#container_factor_'+id).prepend(
                    '<div class="label '+type+' pull-right">Voto  : '+ valor +'</div>'
                )
            }
        })
    });

    function update(value,elem,id){
        child = elem.children('div');
        $input = $('#id_voto-'+id);
        if(value < 0){
            child.removeClass('deg-success').addClass('deg-warning');
            elem.slider('option','range','max');
        }else if(value>0){
            child.addClass('deg-success').removeClass('deg-warning');
            //child.css('background','#44c636','important');
            elem.slider('option','range','min');
        }else{
            child.css('background','rgb(223, 223, 223);','important')
        }
        $input.attr('value',value);
    }
});

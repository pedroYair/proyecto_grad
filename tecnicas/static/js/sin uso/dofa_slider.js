$(function(){
    $for_slide = $('.sld');
    for(i=0;i<$for_slide.length;i++){
        var slug = $($for_slide[i]).data('sld');
        $('#id_valoracion_'+slug).parent().append('<div class="row">' +
        '<label class="col-md-3">Valoración</label>' +
        '<div class="col-md-7 mtop-5">' +
        '<div id="'+slug+'">' +
        '</div>' +
        '</div>' +
        '</div>');
        $slide = $('#'+slug);
        $slide.slider({
            min: -5,
            max: 5,
            value: 0,
            animate: true,
            range: "min",
            slide: function( event, ui ) {
                update(ui.value,$(ui.handle).parent(),slug)
            }
        });
    }
});

function update(value,elem,slug){
    child = elem.children('div');
    $input = $('#id_valoracion_'+slug);
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
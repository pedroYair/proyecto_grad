console.log('Loading CrearFuenteFormController');

$(function () {
    $('#crear_evidencia').on('click', function (evt) {
        evt.preventDefault();
        var $form = $('#creacion_fuente_form');
        $form.submit();
    });

    $('#creacion_fuente_form')
        .submit(function (e) {
            $.ajax({
                url: $(this).attr('action'),
                type: 'POST',
                data: new FormData(this),
                processData: false,
                contentType: false,
                success: function (data, textStatus, jqXHR) {
                    if (data.done) {
                        clean_django_error('#creacion_fuente_form');
                        imprimir_mensaje('.all','Fuente creada con éxito','success');
                        var $conteo = $('#conteo-'+data.prediccion);
                        console.log($conteo);
                        $conteo.html(parseInt($conteo.html())+1);
                    } else {
                        report_django_error_input(data.errors, '#creacion_fuente_form')
                    }
                }
            });
            e.preventDefault();
        });
});
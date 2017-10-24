$(function () {
    var $modal_reglas = $('#modal_reglas');
    $('.lista-lluvia-ideas').on('click', '.lluvia_idea .mostrar-reglas', function () {
        var id_lluvia_ideas = $(this).attr('data-id');
        var titulo = $('.lluvia_idea[data-id=' + id_lluvia_ideas + ']').find('.lluvia_idea_titulo').html();
        $modal_reglas.find('.modal-title').html(titulo);
        $modal_reglas.find('.modal-body').find('ul').remove();
        $modal_reglas.find('.modal-body').find('input[type=text]').attr('disabled', 'disabled');
        $modal_reglas.find('.modal-body').find('#id_form_regla-lluvia_ideas').val(id_lluvia_ideas);
        $modal_reglas.modal('show');
        $.getJSON(url_ver_reglas_lluvia_ideas, {lluvia_ideas: id_lluvia_ideas}, function (data) {
            $modal_reglas.find('.modal-body').append(data['html']);
            $modal_reglas.find('.modal-body').find('input[type=text]').removeAttr('disabled');

        }).fail(function () {
            $modal_reglas.find('.modal-body').find('input[type=text]').removeAttr('disabled');
        });
    });

    $('.lista-lluvia-ideas').on('click', '.lluvia_idea .delete-lluvia-ideas', function () {
        var id_lluvia_ideas = $(this).attr('data-id');
        swal({
                title: "¿Desea eliminar la lluvia de ideas y todas sus sesiones?",
                //text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: "btn-danger",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {

                if (isConfirm) {
                    $.post(url_eliminar_lluvia_ideas, {'lluvia_ideas': id_lluvia_ideas}, function (data) {
                        if (!data['error']) {
                            swal('Eliminado', 'Se ha eliminado con exito la lluvia de ideas.', 'success');
                            $('.lluvia_idea[data-id=' + id_lluvia_ideas + ']').parent().remove();
                        } else {

                        }
                    }).fail(function () {
                        swal('Error', 'Lo sentimos, no se pudo eliminar la lluvia de ideas.', 'error');
                    });
                } else {
                    swal('Cancelado', 'No se ha eliminado la lluvia de ideas', 'error');
                }
            });
    });

    $('.sesiones').on('click', '.sesion .eliminar-sesion', function () {
        //var flag = confirm('¿Desea reabrir la sesion?');
        var id_sesion = $(this).data('id');

        swal({
                title: "¿Desea eliminar la sesión seleccionada de lluvia de ideas?",
                //text: "You will not be able to recover this imaginary file!",
                type: "warning",
                showCancelButton: true,
                confirmButtonClass: "btn-danger",
                confirmButtonText: "Eliminar",
                cancelButtonText: "Cancelar",
                closeOnConfirm: false,
                closeOnCancel: false
            },
            function (isConfirm) {

                if (isConfirm) {
                    $.post(url_eliminar_sesion, {'sesion': id_sesion}, function (data) {
                        if (!data['error']) {
                            swal('Eliminado', 'Se ha eliminado con exito la sesion.', 'success');
                            $('.sesion[data-id=' + id_sesion + ']').remove();
                        } else {

                        }
                    }).fail(function () {
                        swal('Error', 'Lo sentimos, no se pudo eliminar la sesion.', 'error');
                    });
                } else {
                    swal('Cancelado', 'No se ha eliminado la sesion', 'error');
                }
        });
    });

    $('.sesiones').on('click', '.sesion .abrir-sesion', function () {
        var id_sesion = $(this).attr('data-id');
        swal({
            title: "¿Desea reabrir la sesion?",
            //text: "You will not be able to recover this imaginary file!",
            type: "info",
            showCancelButton: true,
            confirmButtonClass: "btn-primary",
            confirmButtonText: "Abrir",
            cancelButtonText: "Cancelar",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {

            if (isConfirm) {
                $.post(url_abrir_sesion, {'sesion': id_sesion}, function (data) {
                    if (!data['error']) {
                        swal('Sesion Abierta', 'Se ha reabierto la sesion con exito.', 'success');
                        $('.sesion[data-id=' + id_sesion + ']').removeClass('cerrado');
                        $('.sesion[data-id=' + id_sesion + ']').find('.cerrar-sesion').show();
                        $('.sesion[data-id=' + id_sesion + ']').find('.abrir-sesion').hide();
                    } else {
                        swal('Cancelado', 'No se pudo abrir la sesion', 'error');
                    }
                }).fail(function () {
                    swal('Cancelado', 'No se pudo abrur la sesion', 'error');
                });
            } else {
                swal('Cancelado', 'No se ha abierto la sesion', 'error');
            }
        });
    });

    $('.sesiones').on('click', '.sesion .cerrar-sesion', function () {
        var id_sesion = $(this).attr('data-id');
        swal({
            title: "¿Desea cerrar la sesion?",
            //text: "You will not be able to recover this imaginary file!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn-danger",
            confirmButtonText: "Cerrar",
            cancelButtonText: "Cancelar",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {

            if (isConfirm) {
                //$.post(url_cerrar_sesion, {'sesion': id_sesion}, function (data) {
                //    if (!data['error']) {
                //        swal('Sesion Cerrada', 'Se ha cerrado la sesion con exito.', 'success');
                //        $('.sesion[data-id=' + id_sesion + ']').addClass('cerrado');
                //        $('.sesion[data-id=' + id_sesion + ']').find('.cerrar-sesion').hide();
                //        $('.sesion[data-id=' + id_sesion + ']').find('.abrir-sesion').show();
                //    } else {
                //        swal('Cancelado', 'No se pudo cerrar la sesion', 'error');
                //    }
                //}).fail(function () {
                //    swal('Cancelado', 'No se pudo cerrar la sesion', 'error');
                //});
                location.href = url_cerrar_sesion.replace('0', id_sesion)
            } else {
                swal('Cancelado', 'No se ha cerrado la sesion', 'error');
            }
        });
    });

    $('.sesiones').on('click', '.sesion .no-permitir-ideas', function () {
        var id_sesion = $(this).attr('data-id');
        swal({
            title: "¿Cerrar creacion de ideas?",
            //text: "You will not be able to recover this imaginary file!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn-danger",
            confirmButtonText: "Cerrar",
            cancelButtonText: "Cancelar",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {

            if (isConfirm) {
                $.post(url_no_permitir_ideas, {'sesion': id_sesion}, function (data) {
                    if (!data['error']) {
                        swal('Creacion de Ideas ', 'Se ha cerrado la creacion de ideas', 'success');
                        //$('.sesion[data-id=' + id_sesion + ']').addClass('cerrado');
                        $('.sesion[data-id=' + id_sesion + ']').find('.no-permitir-ideas').hide();
                        $('.sesion[data-id=' + id_sesion + ']').find('.permitir-ideas').show();
                    } else {
                        swal('Cancelado', 'No se pudo cerrar la creacion de ideas', 'error');
                    }
                }).fail(function () {
                    swal('Cancelado', 'No se pudo cerrar la creacion de ideas', 'error');
                });
            } else {
                swal('Cancelado', 'Ha cancelado el cerrado de la creacion de ideas', 'error');
            }
        });
    });

    $('.sesiones').on('click', '.sesion .permitir-ideas', function () {
        var id_sesion = $(this).attr('data-id');
        swal({
            title: "¿Abrir creacion de ideas?",
            //text: "You will not be able to recover this imaginary file!",
            type: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn-danger",
            confirmButtonText: "Abrir",
            cancelButtonText: "Cancelar",
            closeOnConfirm: false,
            closeOnCancel: false
        },
        function (isConfirm) {

            if (isConfirm) {
                $.post(url_permitir_ideas, {'sesion': id_sesion}, function (data) {
                    if (!data['error']) {
                        swal('Creacion de Ideas ', 'Se ha abierto la creacion de ideas', 'success');
                        //$('.sesion[data-id=' + id_sesion + ']').addClass('cerrado');
                        $('.sesion[data-id=' + id_sesion + ']').find('.permitir-ideas').hide();
                        $('.sesion[data-id=' + id_sesion + ']').find('.no-permitir-ideas').show();
                    } else {
                        swal('Error', 'No se pudo abrir la creacion de ideas', 'error');
                    }
                }).fail(function () {
                    swal('Error', 'No se pudo abrir la creacion de ideas', 'error');
                });
            } else {
                swal('Cancelado', 'Ha cancelado la apertura de la creacion de ideas', 'error');
            }
        });
    });

    $('.sesiones').on('click', '.sesion .editar-sesion', function () {
        var id_sesion = $(this).attr('data-id');
        $.getJSON(url_obtener_sesion, {sesion: id_sesion}, function(data){
            if(data.sesion.abierto){
                $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-abierto').attr('checked', 'checked');
            }else{
                $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-abierto').removeAttr('checked');
            }

            if(data.sesion.permitir_ideas){
                $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-permitir_ideas').attr('checked', 'checked');
            }else{
                $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-permitir_ideas').removeAttr('checked');
            }

            $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-id').val(data.sesion.id);
            $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-codigo').val(data.sesion.codigo);
            $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-fecha_inicio').val(data.sesion.fecha_inicio);
            $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-fecha_final').val(data.sesion.fecha_final);
            $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-lluvia_ideas').val(data.sesion.lluvia_ideas);

            $('#modal_editar_sesion').modal()
        });
    });

    $('#btn_editar_sesion').on('click', function(){

            $.post(url_editar_sesion_lluvia_ideas, $('#modal_editar_sesion').find('#form_editar_sesion').serialize(), function(data){
                if(data['error']){
                    var errors = data.errors;
                    for(var i=0; i < errors.length; i++){
                        var field_selector = '';

                        if(errors[i][0] == '__all__'){
                            field_selector = '.' + errors[i][0];
                        }else{
                            field_selector = '[name=form_sesion_edit-' + errors[i][0] + ']';
                        }

                        var field_errors = errors[i][1];
                        var html = '<ul class="errorlist">';
                        for(var j = 0; j < field_errors.length; j++){
                            html += '<li>' + field_errors[j] + '</li>';
                        }
                        html += '</ul>';

                        $('#modal_editar_sesion').find('#form_editar_sesion').find(field_selector).after(html);


                    }
                }else{
                    $('#modal_editar_sesion').find('#form_editar_sesion').find('.errorlist').remove();
                    $('#modal_editar_sesion').find('#form_editar_sesion').find('.__all__').html('');

                    var id_sesion =  $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-id').val();
                    var codigo =  $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-codigo').val();
                    var abierto =  $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-abierto').is(':checked');
                    var permitir_ideas =  $('#modal_editar_sesion').find('#form_editar_sesion').find('#id_form_sesion_edit-permitir_ideas').is(':checked');
                    var $sesion = $('.sesion[data-id='+ id_sesion +']');
                    if (abierto){
                        $sesion.removeClass('cerrado');
                        $sesion.find('.abrir-sesion').hide();
                        $sesion.find('.cerrar-sesion').show();
                    }else{
                        $sesion.addClass('cerrado');
                        $sesion.find('.cerrar-sesion').hide();
                        $sesion.find('.abrir-sesion').show();
                    }
                    if(permitir_ideas){
                        $sesion.find('.permitir-ideas').hide();
                        $sesion.find('.no-permitir-ideas').show();
                    }else{
                        $sesion.find('.no-permitir-ideas').hide();
                        $sesion.find('.permitir-ideas').show();

                    }

                    $sesion.find('>span').html(codigo);
                    swal('Actualizado', 'Se ha actualizado correctamente la sesion.', 'success');
                }
            });
    });

    $modal_reglas.on('click', '#nueva_regla', function () {

        $.post(url_nueva_regla_lluvia_ideas, $('#form_nueva_regla').serialize(), function (data) {
            if (!data['error']) {
                $modal_reglas.find('.modal-body').find('ul').append(data['html']);
                $modal_reglas.find('.modal-body').find('input[type=text]').val('');
            } else {

            }
        }).fail(function () {
            alert('Lo sentimos, no se pudo eliminar la lluvia de ideas.');
        });

    });

    $('#form_nueva_regla').on('submit', function (e) {
        e.preventDefault();
    });

    $('#form_nueva_regla').on('keyup', 'input[type=text]', function (e) {
        if (e.keyCode == 13) {
            $('#form_nueva_regla').find('#nueva_regla').trigger("click");
        }
    });

    $modal_reglas.on('click', '.eliminar-regla', function () {
        var flag = confirm('¿Desea eliminar la regla?');
        var id_regla = $(this).attr('data-id');
        if (flag) {
            $.post(url_eliminar_regla_lluvia_ideas, {regla: id_regla}, function (data) {
                if (!data['error']) {
                    alert('Se ha eliminado con exito la regla seleccionada.');
                    $('.regla[data-id=' + id_regla + ']').remove();
                } else {

                }
            }).fail(function () {
                alert('Lo sentimos, no se pudo eliminar la regla seleccionada.');
            });
        }
    });

    $('#modal_nueva_sesion').find('#id_form_sesion-usar_sesion').on('change', function(){
        var id_sesion = $(this).val();
        if(id_sesion == ""){
            $('#modal_nueva_sesion').find('table').hide();
            $('#modal_nueva_sesion').find('#id_form_sesion-ideas_a_seleccionar').attr('disabled', 'disabled');
        }else{
            $('#modal_nueva_sesion').find('table').show();

            $('#modal_nueva_sesion').find('table').find('tbody').html('');
            $.getJSON(url_ideas_sesiones_por_votos, {sesion: id_sesion}, function(data){
                $('#modal_nueva_sesion').find('table').find('tbody').html(data['html']);
                if(data['count'] > 0){
                    $('#modal_nueva_sesion').find('#id_form_sesion-ideas_a_seleccionar').removeAttr('disabled');
                }else{
                    $('#modal_nueva_sesion').find('#id_form_sesion-ideas_a_seleccionar').attr('disabled', 'disabled');
                }
            });
        }

    });

    $('#modal_nueva_sesion').find('#btn_crear_sesion').on('click', function(){
        var num_items = $('#modal_nueva_sesion').find('table').find('input[name=brain_item]').length;
        var id_lluvia_ideas = $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-lluvia_ideas').val();
        var items_seleccionados = 0;
        var lista_items_seleccionados = [];
        var crear_idea = true;
        if(num_items > 0){
            items_seleccionados = $('#modal_nueva_sesion').find('table').find('input[name=brain_item]:checked').length;
            if(items_seleccionados <= 0){
                swal({
                    title: "¿Esta seguro de crear la sesion sin seleccionar ninguna idea?",
                    //text: "You will not be able to recover this imaginary file!",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonClass: "btn-danger",
                    confirmButtonText: "Aceptar",
                    cancelButtonText: "Cancelar",
                    closeOnConfirm: false,
                    closeOnCancel: false
                },
                function (isConfirm) {
                    crear_idea = isConfirm
                });
            }
        }else{
            crear_idea = true;
        }

        if(crear_idea){
            $.each($('#modal_nueva_sesion').find('table').find('input[name=brain_item]:checked'), function(index, item){
                lista_items_seleccionados.push($(this).val());
            });
            var data_send = {
                'form_sesion-lluvia_ideas': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-lluvia_ideas').val(),
                'form_sesion-codigo': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-codigo').val(),
                'form_sesion-abierto': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-abierto').is(':checked'),
                'form_sesion-permitir_ideas': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-permitir_ideas').is(':checked'),
                'form_sesion-fecha_inicio': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-fecha_inicio').val(),
                'form_sesion-fecha_final': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-fecha_final').val(),
                'form_sesion-usar_sesion': $('#modal_nueva_sesion').find('#form_nueva_sesion').find('#id_form_sesion-usar_sesion').val(),
                'items_seleccionados': lista_items_seleccionados
            };
            $('#modal_nueva_sesion').find('#form_nueva_sesion').find('.errorlist').remove();
            $.post(url_nueva_sesion_lluvia_ideas, data_send, function(data){
                if(data['error']){
                    var errors = data.errors;
                    for(var i=0; i < errors.length; i++){
                        var field_selector = '';

                        if(errors[i][0] == '__all__'){
                            field_selector = '.' + errors[i][0];
                        }else{
                            field_selector = '[name=form_sesion-' + errors[i][0] + ']';
                        }

                        var field_errors = errors[i][1];
                        var html = '<ul class="errorlist">';
                        console.log(field_selector);
                        console.log(field_errors);
                        for(var j = 0; j < field_errors.length; j++){
                            html += '<li>' + field_errors[j] + '</li>';
                        }
                        html += '</ul>';

                        $('#modal_nueva_sesion').find('#form_nueva_sesion').find(field_selector).after(html);

                    }
                }else{
                    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('.errorlist').remove();
                    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('.__all__').html('');
                    $('.lluvia_idea[data-id='+ id_lluvia_ideas +']').find('.widget-content').find('.sesiones').append(data['sesion_html'])
                    $('#modal_nueva_sesion').modal('hide');
                }
            });
        }

    });



    $('#modal_nueva_sesion').find('#id_form_sesion-ideas_a_seleccionar').on('input', function(){
        var ideas_a_seleccionar = parseInt($(this).val());
        console.log(ideas_a_seleccionar);
        $('#modal_nueva_sesion').find('table').find('input[name=brain_item]').removeAttr('checked');
        for(var i=0; i < ideas_a_seleccionar; i++){
            $('#modal_nueva_sesion').find('table').find('input[name=brain_item][data-count='+ i +']').attr('checked', 'checked');
        }
    });

    $('.lista-lluvia-ideas').on('click', '.lluvia_idea .add-sesion', function () {
        clean_nueva_sesion_form();
        var id_lluvia_ideas = $(this).attr('data-id');
        $('#modal_nueva_sesion').find('#id_form_sesion-usar_sesion').html('');
        $('#modal_nueva_sesion').find('#id_form_sesion-lluvia_ideas').val(id_lluvia_ideas);
        $.getJSON(url_sesiones_lluvia_ideas, {lluvia_ideas: id_lluvia_ideas}, function(data){
            $('#modal_nueva_sesion').find('#id_form_sesion-usar_sesion').html(data['html']);
            console.log(data['count']);
            if(data['count'] <= 0){
                //$('#modal_nueva_sesion').find('table').hide();
                $('#modal_nueva_sesion').find('#id_form_sesion-usar_sesion').attr('disabled', 'disabled');
                $('#modal_nueva_sesion').find('#id_form_sesion-ideas_a_seleccionar').attr('disabled', 'disabled');
            }else{
                //$('#modal_nueva_sesion').find('table').show();
                $('#modal_nueva_sesion').find('#id_form_sesion-usar_sesion').removeAttr('disabled');
                $('#modal_nueva_sesion').find('#form_sesion-ideas_a_seleccionar').removeAttr('disabled');
            }
        });
        $('#modal_nueva_sesion').modal();

    });

    $('#id_form_sesion-fecha_inicio').datepicker({

        calendarWeeks: true,
        format: "dd/mm/yyyy",
        language: 'es',
        startDate: "{{ today|date:'d/m/Y' }}",
        autoclose: true,

    }).on('changeDate', function (e) {
        $('#id_form_sesion-fecha_final').focus();
    });

    $('#id_form_sesion-fecha_final').datepicker({
        calendarWeeks: true,
        format: "dd/mm/yyyy",
        language: 'es',
        startDate: "{{ today|date:'d/m/Y' }}",
        autoclose: true
    }).on('changeDate', function (e) {

    });

    $('#id_form_sesion_edit-fecha_inicio').datepicker({

        calendarWeeks: true,
        format: "dd/mm/yyyy",
        language: 'es',
        //startDate: "{{ today|date:'d/m/Y' }}",
        autoclose: true,

    }).on('changeDate', function (e) {
        $('#id_form_sesion_edit-fecha_final').focus();
    });

    $('#id_form_sesion_edit-fecha_final').datepicker({
        calendarWeeks: true,
        format: "dd/mm/yyyy",
        language: 'es',
        //startDate: "{{ today|date:'d/m/Y' }}",
        autoclose: true
    }).on('changeDate', function (e) {

    });
});

function clean_nueva_sesion_form(){
    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('.errorlist').remove();
    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('.__all__').html('');
    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('input').val('');
    $('#modal_nueva_sesion').find('#form_nueva_sesion').find('select').val('');
}
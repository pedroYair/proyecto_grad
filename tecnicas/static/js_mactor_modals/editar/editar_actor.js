
// se cargan los datos en las cajas de texto respectivas
    $(document).ready(function () {
        $("a").click(function () {
            // se obtiene el id del actor para realizar la consulta, el cual fue asignado a la etiquera <a>
            var id = $(this).attr("id");
            if(id != undefined && id.indexOf("edi")!= -1)
            {
                // se elimina la subcadena edi
                id = id.substring(3);
                // se asigna como id del boton actualizar el id del actor para cuando se pulse el boton actualizar
                $('#modal_actualizar').val(id);
                    //idEstudio = 0 para que cumpla la expresion de la url
                    $.ajax(
                        {
                            data: {'id': id, 'idEstudio': 0},
                            url: 'consultar_actor',
                            type: 'get',
                            // los datos retornados son asignados en el formulario
                            success: function (data) {
                                var object = JSON.parse(data);
                                document.getElementById("nombreLargo2").value = object.nombreLargo;
                                document.getElementById("nombreCorto2").value = object.nombreCorto;
                                document.getElementById("descripcion2").value = object.descripcion;
                            }
                        });

            }

        });


    });

// funcion que actualiza el registro del actor al presionar el boton actualizar
function actualizar() {
        // se obtienen los datos actualizados
        var id = $('button[id=modal_actualizar]').val();
        var nombreLargo = $('input[name="nombreLargo2"]').val();
        var nombreCorto = $('input[name="nombreCorto2"]').val();
        var descripcion = $('textarea[name="descripcion2"]').val();
        var estudio = $('input[name="idEstudio"]').val();

        if(nombreCorto=="" || nombreLargo=="")
        {
        alert("Ingrese todos los datos")
        }
        // si los datos estan completos se envian mediante ajax
        else
        {
            $.ajax({
                data: {
                    'id': id,
                    'nombreLargo': nombreLargo,
                    'nombreCorto': nombreCorto,
                    'descripcion': descripcion,
                    'idEstudio': estudio
                },
                url: 'editar_actor',
                type: 'get',
                // se obtiene e imprime en el modal la respuesta
                success: function (data) {
                    var object = JSON.parse(data);
                    var html = "<p>" + object.info + "</p>";
                    $('#mod_body3').html(html);
                    // se desactiva el boton actualizar
                    document.getElementById('modal_actualizar').disabled = true;
                }
            });
        }

    }





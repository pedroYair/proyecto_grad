
// se cargan los datos en las cajas de texto respectivas
    $(document).ready(function () {
        $("a").click(function () {
            // se obtiene el id del objetivo, el cual fue asignado a la etiquera <a>
            var id = $(this).attr("id");
            if(id != undefined && id.indexOf("edi")!= -1)
            {
                id = id.substring(3);
                // se asigna como id del boton actualizar el id del actor
                $('#modal_actualizar').val(id);
                // se envia el id del actor mediante ajax para obtener los datos
                $.ajax(
                    {
                        data: {'id': id},
                        url: 'consultar_objetivo',
                        type: 'get',
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

// funcion que actualiza el registro del actor seleccionado
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
        // si los datos estan completos se envian con ajax
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
                url: 'editar_objetivo',
                type: 'get',
                success: function (data) {
                    var object = JSON.parse(data);
                    // se coloca en el modal la respuesta obtenida
                    var html = "<p>" + object.info + "</p>";
                    $('#mod_body3').html(html);
                    document.getElementById('modal_actualizar').disabled = true;
                }
            });
        }

    }





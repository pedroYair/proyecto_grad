// Mediante este archivo al seleccionar una opcion del primer select (Y), se muestran en el segundo activas solo
// aquellas opciones que aun no se han registrado.

$('#id_idActorY').on('change', DescripcionY);
        function  DescripcionY()
        {   // se obtiene el id del actor
            var id = $(this).val();
            // se obtiene el id del formulario
            var tipo = $(this).closest("form").attr('id');

            $.ajax({
                data : {'id' : id, 'tipo': tipo},
                url : 'mid-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    // permite que al cambiar la opcion se activen las opciones correspondientes (actualizar opciones)
                    for(var i=0; i<object.actores.length;i++)
                    {
                        $("#id_idActorX").find("option[value='"+object.actores[i]+"']").prop("disabled",false);
                    }
                    // al activar todas las opciones se establecen cuales deben desactivarse para la opcion actual
                    for (var i=0;i<object.lista.length; i++)
                    {
                        $("#id_idActorX").find("option[value='"+object.lista[i]+"']").prop("disabled",true);
                    }
                    // se activa el segundo select
                        document.getElementById("id_idActorX").disabled = false;
                }
            });
        }




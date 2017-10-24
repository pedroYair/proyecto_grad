// JS que tiene como funcion desactivar la opcion seleccionado en el select contrario para evitar
// que se ingrese un registro de influencia mid de un actor sobre si mismo.

// para el primer select
$("#id_idActorY").on("change",function(){
    // se obtiene el valor de la opcion seleccionada
        var valor=$(this).val();
    // se desactiva la opcion equivalente en el otro select
        $("#id_idActorX").find("option[value='"+valor+"']").prop("disabled",true);
    // cuando se cambia la opcion se activan nuevamente las opciones bloqueadas
        $("#id_idActorX").find("option[value!='"+valor+"']").prop("disabled",false);
    });

// para el segundo select
$("#id_idActorX").on("change",function(){
        var valor=$(this).val();
        $("#id_idActorY").find("option[value='"+valor+"']").prop("disabled",true);
        $("#id_idActorY").find("option[value!='"+valor+"']").prop("disabled",false);
    });





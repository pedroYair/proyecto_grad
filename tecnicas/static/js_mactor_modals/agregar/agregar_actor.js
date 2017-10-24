/**
 * Created by Win 10 on 12/09/2017.
 */

//Recoje la informacion ingresada y la envia a la url estblecida para guardar
 function guardar() {
        // obtencion de los valores a guardar
        var nombreLargo = $('input[name="nombreLargo"]').val();
        var nombreCorto = $('input[name="nombreCorto"]').val();
        var descripcion = $('textarea[name="descripcion"]').val();
        var codigo_Estudio = $('input[name="codigo_Estudio"]').val();

         if(nombreCorto=="" || nombreLargo=="" || codigo_Estudio=="")
        {
        alert("Ingrese todos los datos");
        }
        else
         {
             // envio de los valores mediante ajax
             $.ajax({
                 data: {
                     'nombreLargo': nombreLargo,
                     'nombreCorto': nombreCorto,
                     'descripcion': descripcion,
                     'codigo_Estudio': codigo_Estudio
                 },
                 url: 'new-actor',
                 type: 'get',
                 // obtencion e impresion de la respuesta
                 success: function (data) {
                     var object = JSON.parse(data);
                     var html = "<p>" + object.info + "</p>";
                     $('#mod_body2').html(html);
                     // desactiva el boton de guardar
                     document.getElementById('boton_guardar').disabled = true;
                 }
             });
         }

    }
/**
 * Created by Win 10 on 12/09/2017.
 */

//Recoje la información ingresada y la envia a la url estblecida para guardar
 function guardar() {

        var nombreLargo = $('input[name="nombreLargo"]').val();
        var nombreCorto = $('input[name="nombreCorto"]').val();
        var descripcion = $('textarea[name="descripcion"]').val();
        var codigo_Estudio = $('input[name="idEstudio"]').val();

         if(nombreCorto=="" || nombreLargo=="" || codigo_Estudio=="")
        {
        alert("Ingrese todos los datos");
        }
        else
         {
             $.ajax({
                 data: {
                     'nombreLargo': nombreLargo,
                     'nombreCorto': nombreCorto,
                     'descripcion': descripcion,
                     'codigo_Estudio': codigo_Estudio
                 },
                 url: 'agregar_objetivo',
                 type: 'get',
                 success: function (data) {
                     var object = JSON.parse(data);
                     var html = "<p>" + object.info + "</p>";
                     $('#mod_body2').html(html);
                     document.getElementById('boton_guardar').disabled = true
                 }
             });
         }

    }
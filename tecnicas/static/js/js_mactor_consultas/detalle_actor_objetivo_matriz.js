
// Obtiene la descripcion del actor u objetivo seleccionado

    $(document).ready(function () {
        $("input").click(function () {
            var id = $(this).attr("id")
            //Si se pulsa el input de un actor
             if((id.indexOf("act")!= -1 || id.indexOf("act")== -1) && id.indexOf("obj")== -1) {
                 $.ajax({
                     data: {'id': id},
                     url: 'actor-ajax',
                     type: 'get',
                     success: function (data) {
                         var object = JSON.parse(data);
                         var html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto + "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo + "</p><br><p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p><p>";
                         $('#mod_body').html(html);
                     }
                 });
             }
             // si se pulsa el input de un objetivo
             else
                 {
                 if (id.indexOf("obj") != -1)
                 {
                     $.ajax({
                         data: {'id': id},
                         url: 'objetivo-ajax',
                         type: 'get',
                         success: function (data) {
                             var object = JSON.parse(data);
                             var html = "<p>" + 'Nombre Corto:' +
                                 "</p><p>" + object.nombreCorto +
                                 "</p><br><p>" + 'Nombre Largo:' +
                                 "</p><p>" + object.nombreLargo +
                                 "</p><br><p>" + 'Descripción:' +
                                 "</p><p>" + object.descripcion + "</p><p>";
                             $('#mod_body2').html(html);
                         }
                     });
                 }
                }



        });
    });



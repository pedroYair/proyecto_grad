/**
 * Created by Win 10 on 2/11/2017.
 */

// Obtiene la descripcion del objetivo al pulsar el boton VER

    $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id")
            console.log(id);
            //Si se pulsa el tr de un estudio
                if(id.indexOf("ver")!= -1){
                    console.log(id)
                    $.ajax(
                        {
                            data: {'id': id},
                            url: 'consultar_objetivo',
                            type: 'get',
                            success: function (data) {
                                var object = JSON.parse(data);
                                var html = "<p>" + 'Nombre Corto:' + "</p><p>" + object.nombreCorto +
                                "</p><br><p>" + 'Nombre Largo:' + "</p><p>" + object.nombreLargo +
                                "</p><br><p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p><p>";
                            $('#mod_body4').html(html);
                            }
                        });
                }
        });
    });

/**
 * Created by Win 10 on 2/11/2017.
 */

// Obtiene la descripcion del objetivo al pulsar el boton VER

    $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id");
            if(id!=undefined)
            {
                if(id.indexOf("ver")!= -1)
                {
                    $.ajax(
                        {
                            data: {'id': id},
                            url: 'consultar_ficha',
                            type: 'get',
                            success: function (data) {
                                var object = JSON.parse(data);
                                var html = "<p>" + 'Estrategias del actor:' + "</p><p>" + object.actorY +
                                "</p><br><p>" + 'Sobre el actor:' + "</p><p>" + object.actorX  +
                                "</p><br><p>" + 'Estrategias:' + "</p><p>" + object.estrategia + "</p><p>";
                            $('#mod_body5').html(html);
                            }
                        });
                }
            }
        });
    });

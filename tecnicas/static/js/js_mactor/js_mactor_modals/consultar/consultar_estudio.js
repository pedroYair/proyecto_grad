
// Obtiene la descripcion del estudio seleccionado

    $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id");
            if(id!=undefined && id.indexOf("ver")!= -1)
            {
                id = id.substring(3);
                    $.ajax(
                        {
                            data: {'id': id},
                            url: 'consultar_estudio',
                            type: 'get',
                            success: function (data) {
                                var object = JSON.parse(data);
                                var html = "<p>" + 'Título:' + "</p><p>" + object.titulo +
                                    "</p><br><p>" + 'Descripcion:' + "</p><p>" + object.descripcion + "</p><p>";
                                $('#mod_body').html(html);
                            }
                        });

            }

        });
    });



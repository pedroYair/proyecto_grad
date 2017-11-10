
// Obtiene la descripcion del estudio seleccionado

    $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id")
            console.log(id);
            //Si se pulsa el tr de un estudio
                if(id.indexOf("est")!= -1){
                    console.log(id)
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


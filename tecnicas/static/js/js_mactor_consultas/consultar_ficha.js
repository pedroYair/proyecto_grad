
// Obtiene el registro de la ficha de estrategias de los actores seleccionados

function  Consultar_ficha()
        {
            var id = $(id_idActorX).val();
            var id2 = $(id_idActorY).val();
            $.ajax({
                data : {'id' : id, 'id2' : id2},
                url : 'ficha-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Estrategias:' + "</p><p>" + object.
                            info + "</p>";
                    $('#mod_body').html(html);
                }
            });
        }



// Obtiene la descripcion del actorY seleccionado

$('#id_idActorY').on('change', DescripcionY);
        function  DescripcionY()
        {
            var id = $(this).val();
            $.ajax({
                data : {'id' : id, 'idEstudio': 0},
                url : 'consultar_actor',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Descripción:' + "</p><p>" + object.descripcion + "</p>";
                    $('#info').html(html);
                }
            });
        }

// Obtiene la descripcion del actorX seleccionado

$('#id_idActorX').on('change', DescripcionX);
        function  DescripcionX()
        {
            var id = $(this).val();
            $.ajax({
                data : {'id' : id, 'idEstudio': 0},
                url : 'consultar_actor',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Descripción:' + "</p><p>" + object.
                            descripcion + "</p>";
                    $('#info2').html(html);
                }
            });
        }




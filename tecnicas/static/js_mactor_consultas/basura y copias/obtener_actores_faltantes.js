
// Obtiene la descripcion del actorY seleccionado

$('#id_idActorY').on('change', DescripcionY);
        function  DescripcionY()
        {
            var id = $(this).val();
            var select = document.getElementById("id_idActorY").value; // para saber el valor de select1
            $.ajax({
                data : {'id' : id},
                url : 'mid-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + 'Respuesta:' + "</p><p>" + object.
                            info + "</p>";
                    $('#info2').html(html);
                }
            });
        }





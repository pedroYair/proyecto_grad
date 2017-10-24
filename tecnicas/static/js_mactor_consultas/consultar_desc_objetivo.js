
// Obtiene la descripcion del objetivoX seleccionado

$('#id_idObjetivoX').on('change', Descripcion);
        function  Descripcion()
        {
            var id = $(this).val();
            $.ajax({
                data : {'id' : id},
                url : 'objetivo-ajax',
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



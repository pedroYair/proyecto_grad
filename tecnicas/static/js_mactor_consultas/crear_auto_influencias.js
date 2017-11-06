
// Crea las autoinfluencias para que la matriz sea cuadrada y pueda visualizarse

function autoinfluencia() {

    var idEstudio = $('input[name="idEstudio"]').val();
            $.ajax({
                data : {'idEstudio' : idEstudio},
                url : 'auto_influencia',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    console.log(object.resp);
                }
            });
}



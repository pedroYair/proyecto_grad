
// Crea las autoinfluencias para que la matriz sea cuadrada y pueda visualizarse

function autoinfluencia() {

    var id = "matriz";
            console.log(id);
            $.ajax({
                data : {'id' : id},
                url : 'auto-influencia',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    console.log(object.resp);
                }
            });
    console.log("holaaaaaaaaaaaaaa");
}



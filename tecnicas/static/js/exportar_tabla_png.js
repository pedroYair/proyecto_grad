/**
 * Created by Win 10 on 27/11/2017.
 */

    var element = $("#div_tabla"); // global variable
    var getCanvas; // global variable

    $("#png").on('click', function () {

        var id = $(this).attr("id");
        html2canvas(element, {onrendered: function (canvas) {
                getCanvas = canvas;
             }
         });
    });

    $("#png").on('click', function () {
    var name = $(this).attr("name");
    var imgageData = getCanvas.toDataURL("image/png");
    var newData = imgageData.replace(/^data:image\/png/, "data:application/octet-stream");
    if( name == "actores")
    {
       $("#png").attr("download", "tabla_actores.png").attr("href", newData);
    }
    else
    {
        if(name == "fichas")
        {
           $("#png").attr("download", "fichas_estrategia.png").attr("href", newData);
        }
        else
        {
           $("#png").attr("download", "tabla_objetivos.png").attr("href", newData);
        }
    }

});

/**
 * Created by Win 10 on 27/11/2017.
 */

    var element = $("#div_actores"); // global variable
    var getCanvas; // global variable

    $("#png").on('click', function () {
         html2canvas(element, {
         onrendered: function (canvas) {
                getCanvas = canvas;
             }
         });
    });

    $("#png").on('click', function () {
    var imgageData = getCanvas.toDataURL("image/png");
    var newData = imgageData.replace(/^data:image\/png/, "data:application/octet-stream");
    $("#png").attr("download", "tabla_actores.png").attr("href", newData);
});

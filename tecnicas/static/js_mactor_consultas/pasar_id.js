
 // Obtiene la descripcion del estudio seleccionado
 function pasar_id() {

     $(document).ready(function () {
        $("a").click(function () {
            var id = $(this).attr("id")

            document.location.href = "lista_actores/"+id;
            document.getElementById("id_estudio").text = 1

        });
    });

 }






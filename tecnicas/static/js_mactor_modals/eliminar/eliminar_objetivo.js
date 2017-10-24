
//
var nombre_boton_eliminar = ".delete"; // Clase

  $(document).on('ready',function(){
      // Coloca el nombre del actor seleccionado en la etiqueta id = modal_name
      // <p>¿Realmente desea eliminar al actor <span id="modal_name"></span>?</p>
        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            $('#modal_idButton').val(Pid); // se asigna al boton eliminar con id modal_idProducto el valor Pid
            $('#modal_name').text(name);
        });
    });

 //Elimina el objetivo
function Eliminar(){
      $(document).ready(function(){
          var id = $(modal_idButton).val()
            console.log(id);
            $.ajax({
                data : {'id' : id},
                url : 'eliminar_objetivo-ajax',
                type : 'get',
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + object.
                            info + "</p>";
                    $('#mod_body').html(html);
                    document.getElementById('modal_idButton').disabled = true
                }
            });
        }) ;

}





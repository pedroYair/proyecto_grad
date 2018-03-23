// se obtiene mediante el atributo class el elemento que contiene el id del actor a eliminar
var nombre_boton_eliminar = ".delete";

// Coloca el nombre del actor seleccionado en la etiqueta id = modal_name
      // <p>¿Realmente desea eliminar al actor <span id="modal_name"></span>?</p>
  $(document).on('ready',function(){
        $(nombre_boton_eliminar).on('click',function(e){
            e.preventDefault();
            // se obtienen el id y nombre del actor a eliminar
            var Pid = $(this).attr('id');
            var name = $(this).data('name');
            // se asigna al id del boton eliminar del modal el valor Pid
            $('#modal_idProducto').val(Pid);
            // asigna el nonbre del actor a eliminar a la pregunta de confirmacion
            $('#modal_name').text(name);
        });
    });

 //Elimina al actor al presionar el boton eliminar del modal
function Eliminar(){
      $(document).ready(function(){
          // se obtiene el id del actor a eliminar asignado previamente como id del boton eliminar del modal
          var id = $(modal_idProducto).val();
          // se envia el id mediante ajax
            $.ajax({
                data : {'id' : id},
                url : 'eliminar_actor',
                type : 'get',
                // se obtiene e imprime la respuesta
                success : function (data)
                {
                    var object = JSON.parse(data);
                    var html = "<p>" + object.info + "</p>";
                    $('#mod_body').html(html);
                    // se desactiva el boton eliminar del modal
                    document.getElementById('modal_idProducto').disabled = true;
                }
            });
        }) ;

}





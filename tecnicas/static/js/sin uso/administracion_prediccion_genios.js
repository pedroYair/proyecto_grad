console.log('Cargando controlador para administración Estudio predicción de genios...');

$(function () {
    $('#guardar').click(function (evt) {
        evt.preventDefault();
        $('#admin_form').submit();
    });
    $('#finalizar').click(function(evt){
        evt.preventDefault();
        $('#id_finalizado').prop('checked',true);
        $('#admin_form').submit();
    })
});
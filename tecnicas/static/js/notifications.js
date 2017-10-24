/**
 * Created with PyCharm.
 * User: minrock
 * Date: 7/28/13
 * Time: 2:37 AM
 * To change this template use File | Settings | File Templates.
 */
function new_notification(data){
    //alert(data.titulo +''+data.descripcion );
    //popupNotification(data.msg);
    datos = {
        'titulo':data.titulo,
        'descripcion':data.descripcion,
        'fecha': moment().format('LLL'),
        'url' : data.url
    };

    if(data.type == "notification"){
        $notbadg = $("#notifications-badge");
        var count = parseInt($notbadg.html()) + 1;
        $notbadg.html(count);
        //data.fecha = moment('LLL');
        $tmp = swig.compile($("#not-tpl").html());

        html = $tmp(datos);
        $(html).insertAfter("#nots-list");
        var image = '/static/img/icons/emblem-notice.png'

    }else if(data.type == "message"){
        $mesbadg = $("#messages-badge");
        var count = parseInt($mesbadg.html()) + 1;
        $mesbadg.html(count);
        var image = "/static/img/icons/document-send.png";
        $tmp = swig.compile($("#mess-tpl").html());
        html = $tmp(datos);
        $(html).insertAfter("#mess-list");
    }

    $.gritter.add({
        title:datos.titulo,
        text: datos.descripcion,
        time: 5000,
        sticky: false,
        image : image
    });
}

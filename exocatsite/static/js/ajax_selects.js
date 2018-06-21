$(document).ready(function(){


    // select para la varietat (ojo que este es diferente a los demas,ver funcion de views)
    $.getJSON('/ajax_varietat_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['varietat'] + '">' + data[x]['varietat'] + '</option>';
        }
        $('#varietat').html(options);
    });

    // select para los grups
    $.getJSON('/ajax_grups_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#grups').html(options);
    });

    // select para las vies d'entrada
//    $.getJSON('/ajax_viaentrada_select/', function(data){
//        var options = '<option value="">-</option>';
//        for (var x = 0; x < data.length; x++) {
//            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
//        }
//        $('#viaentrada').html(options);
//    });
    // select para los estatus
    $.getJSON('/ajax_estatus_catalunya_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#estatuscatalunya').html(options);
    });
    $.getJSON('/ajax_estatus_historic_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#estatushistoric').html(options);
    });
//    // select para las regiones nativas
//    $.getJSON('/ajax_regionativa_select/', function(data){
//        var options = '<option value="">-</option>';
//        for (var x = 0; x < data.length; x++) {
//            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
//        }
//        $('#regionativa').html(options);
//    });


});
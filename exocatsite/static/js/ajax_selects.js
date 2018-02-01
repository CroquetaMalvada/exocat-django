$(document).ready(function(){

    // select para los grups
    $.getJSON('/ajax_grups_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#grups').html(options);
    });

    // select para las vies d'entrada
    $.getJSON('/ajax_viaentrada_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#viaentrada').html(options);
    });
    // select para los estatus (ojo que este se aplica a 2 selects!)
    $.getJSON('/ajax_estatus_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#estatuscatalunya').html(options);
        $('#estatushistoric').html(options);
    });
    // select para las regiones nativas
    $.getJSON('/ajax_regionativa_select/', function(data){
        var options = '<option value="">-</option>';
        for (var x = 0; x < data.length; x++) {
            options += '<option value="' + data[x]['id'] + '">' + data[x]['nom'] + '</option>';
        }
        $('#regionativa').html(options);
    });


});
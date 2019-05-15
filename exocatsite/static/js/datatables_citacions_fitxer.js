/////IDIOMA DATATABLES
var opciones_idioma = {
//    "decimal":        separador_decimales,
//    "thousands":      separador_miles,
    "emptyTable":     "No s'han trobat dades",
    "info":           "Mostrant d'_START_ a _END_ de _TOTAL_ resultats",
    "infoEmpty":      "0 resultats",
    "infoFiltered":   "(filtrats d'un total de _MAX_)",
    "infoPostFix":    "",
    "lengthMenu":     "Mostrar _MENU_ resultats",
    "loadingRecords": "Carregant...",
    "processing":     "Processant...",
    "search":         "Buscar:",
    "zeroRecords":    "No s'han trobat resultats",
    "paginate": {
        "first":      "Primer",
        "last":       "Últim",
        "next":       "Següent",
        "previous":   "Anterior"
    },
    "aria": {
        "sortAscending":  ": activar per ordenar de forma ascendent",
        "sortDescending": ": activar per ordenar de forma descendent"
    }
}

var taula_citacions_fitxer;
var taula_detalls_citacions_fitxer;
$(document).ready(function(){

    // Si se esta cargando especies:
    var dialogcits=$("#dialogdiv").dialog({
            modal:true,
            resizable:true,
            draggable:true,
    //        height: 400,
            width: '80%',
            closeOnEscape:true,
            autoOpen:false,
            show: {effect:"puff", duration:500},
            hide: {effect:"puff", duration:500},
    //        content:$("#dialogdiv"),
    });


    $.fn.dataTable.moment( 'DD-MM-YYYY' ); ///para definir el formato estandar de fechas en las tables(depende de datetime-moment.js y moment.min.js)
    taula_citacions_fitxer = $("#taula_citacions_fitxer").DataTable({
//                    processing:true,
//                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                ajax: {
                    url: '/ajax_citaciones_fichero/',
                    dataSrc: '',
                },
                "deferRender": true,
                columns:[
                    {'data':{'data':'data'},"render": function(data){return data["data"].substring(0,10);}}, //.replace(/-/g,".")
                    {'data': 'data'},
                    {'data': 'usuari'},
                    {'data': 'origen'},
                    {'data':{'id_paquet':'id_paquet'},"render": function(data){return '<a class="btn btn-info info_citacio_fitxer" value="'+data["id_paquet"]+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>';}}
//                        {'data':{'id':'id'},"render": function(data){return '<form action="/formularis_localitats_especie/" method="get"><input value="'+data["id"]+'" hidden/><button class="btn btn-info" title="EDITAR FORMULARI"><i class="fa fa-eye fa-lg"></i></form>';}}
                ],
                columnDefs:[
                    {"visible":false,"targets":[0]},
//                    { type: 'de_date', targets: 0 },
                    { "orderData":[ 0 ],   "targets": [ 1 ] }, //ordenar por la fecha autentica al clicar en la fecha que ve el usuario
                    { "width": "5%", "targets": [4] }//,

                ],
                order: [[ 0, "desc" ]],
                scrollY:        '80vh',
                scrollCollapse: true,
                searching:true,
                autowidth:      true,
                overflow:       "auto",
                language: opciones_idioma,
    });

    taula_detalls_citacions_fitxer = $("#taula_detalls_citacions_fitxer").DataTable({
//                    processing:true,
//                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                ajax: {
                    url: '/json_vacio/',
                    dataSrc: '',
                },
//                "deferRender": true,
                columns:[
                    {'data': 'especie'},
                    {'data': 'coordenada_x'},
                    {'data': 'coordenada_y'},
                    {'data': 'utm1km'},
                    {'data': 'utm10km'},
                    {'data': 'localitat'},
                    {'data': 'municipi'},
                    {'data': 'comarca'},
                    {'data': 'provincia'},
                    {'data': 'data'},
                    {'data': 'autor_s'},
                    {'data': 'observacions'}
                ],
//                columnDefs:[
////                        {"visible":false,"targets":[0]},
//                    { "width": "5%", "targets": [3] }
//                ],
//                order: [[ 1, "asc" ]],
                scrollY:        '80vh',
                scrollCollapse: true,
                searching:true,
                autowidth:      true,
                overflow:       "auto",
                pageLenght:50,
                language: opciones_idioma,
    });
    // ajustar columnas al cargar un tab
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();
    })

    $(document).on( 'click','.info_citacio_fitxer', function (e) {
//        resetear_nav();
//        taula_detalls_citacions_fitxer.ajax.url('/show_lineas_pedido/'+id_pedido+'/');
//        $("#mapa_de_especie").attr("value",$(this).attr("value"));
        var id_paquet=$(this).attr("value");
        $("#dialogdiv").dialog("open");
        taula_detalls_citacions_fitxer.clear();
        $("#loading").show();
        $("#dialog_taula_detalls_citacions_fitxer").hide();
        $.ajax({
            dataType: "json",
            url: '/ajax_mostrar_info_citaciones_fichero/',
            method: 'GET',
            data: {"id":id_paquet},
            success: function(data){
                $("#loading").hide();
                $("#dialog_taula_detalls_citacions_fitxer").show();
                taula_detalls_citacions_fitxer.rows.add(data);
                taula_detalls_citacions_fitxer.columns.adjust().draw();
            },
            error:function(){
                $("#dialogdiv").dialog("close");
            }
        });
    });
//
//        $("#taula_formularis_usuari").on( 'click', '.editar_formulari', function (){
//            $("#id_form").val($(this).attr("value"));
//            $("#form_formularis_usuari").trigger("submit");
//        });
});
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

$(document).on({

    ajaxStart: function(){
        $("#boton_filtrar").hide();
        $("#filtrar_loading").show();
//            if($(this).find(".dataTables_empty")){
//                var mensaje=$(this).find(".dataTables_empty");
//                mensaje.html("Carregant...");
//            }
//            load = loading("Carregant...");
    },
    ajaxStop: function(){
        $("#boton_filtrar").show();
        $("#filtrar_loading").hide();
//            if($(this).find(".dataTables_empty")){
//                var mensaje=$(this).find(".dataTables_empty");
//                mensaje.html("No s'han trobat dades");
//            }

    }
});

var filtros=null;
var taula_especies;
var taula_especies_map
$(document).ready(function(){

    // Si se esta cargando especies:


    taula_especies = $("#taula_especies").DataTable({
//                    processing:true,
//                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                    ajax: {
                        url: '/ajax_taula_especies/',
                        dataSrc: '',
                        type:"POST",
                        data:function(d){
                            d.especie=$("#especie").val();
                            d.grups=$("#grups").val();
                            d.estatuscatalunya=$("#estatuscatalunya").val();
                            d.varietat=$("#varietat").val();
                            d.regionativa=$("#regionativa").val();
                            d.viaentrada=$("#viaentrada").val();
                            d.estatushistoric=$("#estatushistoric").val();
                            d.present_catalog=$("#present_catalog").val();
//                            d.=$("#").val();
                        }
                    },
                    "deferRender": true,
                    columns:[
                        {'data': 'id'},
                        {'data': 'especie'},
                        {'data': 'grup'},
//                        {'data': 'estatuscat'},
//                        {'data': 'varietat'},
//                        {'data': 'regionativa'},
//                        {'data': 'viaentrada'},
//                        {'data': 'estatushistoric'},
//                        {'data': 'present'},
                        {'data':{'id':'id'},"render": function(data){return '<a class="btn btn-info mostrar_info_especie" value="'+data["id"]+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0]},
                        { "width": "5%", "targets": [3] }
                    ],
                    order: [[ 1, "asc" ]],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    searching:false,
//                    "pagingType": "full_numbers",
//                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });

        taula_especies_map = $("#table_info_map").DataTable({
                    columnDefs:[
                        { "width": "5%", "targets": [1] }
                    ],
                    order: [[ 0, "asc" ]],
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    searching:false,
                    autowidth:      true,
                    overflow:       "auto",
                    paging: false,
                    language: opciones_idioma,
        });

        $('a.visibilidad').on( 'click', function (e) {
            e.preventDefault();

            if($(this).children("strike").length>0)
                $(this).html($(this).find("strike").html());
            else
                $(this).html("<strike>"+$(this).html()+"</strike>");

            var column = taula_especies.column( $(this).attr('columna') );

            column.visible( ! column.visible() );
        } );

        // FILTROS PARA LA TABLA!
        $("#form_filtres").submit(function(event){
            event.preventDefault();
            taula_especies.ajax.url("/ajax_taula_especies_filtres/");
            taula_especies.ajax.reload(null,false);

        });
});

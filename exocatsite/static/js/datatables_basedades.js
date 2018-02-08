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
var taula_especies_map;
var taula_especies_info_localitzacio;
var taula_especies_info_masses;
var taula_resum_localitats_especie;
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
                        { "width": "5%", "targets": [1,2] }
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

        taula_resum_localitats_especie = $("#table_resum_localitats_especie").DataTable({
                    columnDefs:[
                        { "width": "20%", "targets": [0] }
                    ],
                    order:false,
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    searching:      false,
                    autowidth:      true,
                    overflow:       "auto",
                    paging: false,
                    language: opciones_idioma,
                    info:false
        });

//        taula_especies_info_localitzacio = $("#taula_localitzacio_info_especie").DataTable({
////                    columnDefs:[
////                        { "width": "30%", "targets": [1,2] }
////                    ],
//                    order: [[ 0, "asc" ]],
//                    scrollY:        '50vh',
//                    scrollCollapse: true,
//                    searching:false,
//                    autowidth:      true,
//                    overflow:       "auto",
//                    paging: false,
//                    language: opciones_idioma,
//        });
//
//        taula_especies_info_masses = $("#taula_localitzacio_info_especie_masses").DataTable({
////                    columnDefs:[
////                        { "width": "30%", "targets": [1,2] }
////                    ],
//                    order: [[ 0, "asc" ]],
//                    scrollY:        '50vh',
//                    scrollCollapse: true,
//                    searching:false,
//                    autowidth:      true,
//                    overflow:       "auto",
//                    paging: false,
//                    language: opciones_idioma,
//        });



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

function cargando_datos_mapa(tipo){
    if(tipo==0){//si se ha empezado a cargar
        taula_especies_map.clear().draw();
        $("#table_info_map").find(".dataTables_empty").html("Buscant dades...") //<img src='https://loading.io/spinners/magnify/lg.searching-for-loading-icon.gif' width='10%'></img>
    }else if(tipo==1){// si ya se han cargado los datos
        $("#table_info_map").find(".dataTables_empty").html("No s'han trobat dades.")
    }else if(tipo==2){// si ha habido un error
        $("#table_info_map").find(".dataTables_empty").html("Error.")
    }

}

function rellenar_table_especies_click(data){ // esta funcion se llama en funciones_leaflet.js
    taula_especies_map.clear();
    $(data).each(function(){

//                    console.log(this);
        var total=this.nutm10000+this.nutm1000+this.ncitacions+this.nmassesaigua
        taula_especies_map.row.add([
            this.nom,
            this.nutm10000,
            this.nutm1000,
            this.ncitacions,
            this.nmassesaigua,
            total,
            '<a class="btn btn-info mostrar_info_especie" value="'+this.id+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>'
        ]).draw();
        //alert(this.properties.IDSPINVASORA);
    });
}
function rellenar_table_especies_seleccion(data){ // esta funcion se llama en funciones_leaflet.js
    taula_especies_map.clear();
    $(data).each(function(){
//                console.log(this);
        var total=this.nutm1000+this.nutm10000+this.ncitacions+this.nmassesaigua

        taula_especies_map.row.add([
            this.nom,
            this.nutm1000,
            this.nutm10000,
            this.ncitacions,
            this.nmassesaigua,
            total,
            '<a class="btn btn-info mostrar_info_especie" value="'+this.id+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>'
        ]);
    });
    taula_especies_map.draw();
}

function rellenar_table_resum_localitats_especie(data){ // esta funcion se llama en info_especie.js
    //taula_resum_localitats_especie.columns(0).clear();
    taula_resum_localitats_especie.cell(0,1).data(data["genere"]+" "+data["especie"]);
    taula_resum_localitats_especie.cell(1,1).data(data["nutm10000"]);
    taula_resum_localitats_especie.cell(2,1).data(data["nutm1000"]);
    taula_resum_localitats_especie.cell(3,1).data(data["ncitacions"]);
    taula_resum_localitats_especie.cell(4,1).data(data["nmassesaigua"]);
    taula_resum_localitats_especie.cell(5,1).data(data["nutm10000"]+data["nutm1000"]+data["ncitacions"]+data["nmassesaigua"]);
    $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();///IMPORTANTE sirve para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
//    $(data["citacions"]).each(function(){
//
//    });
}


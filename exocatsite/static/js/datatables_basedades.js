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
        $("#limpiar_filtros").hide();
        $("#generar_csv").hide();
        $("#filtrar_loading").show();
//            if($(this).find(".dataTables_empty")){
//                var mensaje=$(this).find(".dataTables_empty");
//                mensaje.html("Carregant...");
//            }
//            load = loading("Carregant...");
    },
    ajaxStop: function(){
        $("#boton_filtrar").show();
        $("#limpiar_filtros").show();
        $("#generar_csv").show();
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
var taula_documentacio_especie;
var taula_actuacions_especie;

$(document).ready(function(){

    //$("#data_min_citacio").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false});
    //$("#data_max_citacio").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false});
    for (i = new Date().getFullYear(); i >= 1980; i--){
        $('#data_min_citacio').append($('<option />').val(i).html(i));
        $('#data_max_citacio').append($('<option />').val(i).html(i));
    }
    comprobar_filtrar_data_citacio();
    comprobar_buscar_per();
    // Si se esta cargando especies:


    taula_especies = $("#taula_especies").DataTable({
                    processing:true,
                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                    ajax: {
                        url: '/ajax_taula_especies/',
                        dataSrc: 'data',
                        type:"POST",
                        data:function(d){
                            //d.genere=$("#genere").val();
                            //d.especie=$("#especie").val();
                            //d.subespecie=$("#subespecie").val();
                            d.buscar_per=$("input:radio[name='buscar_per']:checked").val();
                            d.nom_especie=$("#nom_especie").val();
                            d.sinonim_especie=$("#sinonim_especie").val();
                            d.grups=$("#grups").val();
                            d.estatuscatalunya=$("#estatuscatalunya").val();
                            d.varietat=$("#varietat").val();
                            d.regionativa=$("#regionativa").val();
                            d.viaentrada=$("#viaentrada").val();
                            d.estatushistoric=$("#estatushistoric").val();
                            d.present_catalog=$("#present_catalog").val();
                            d.present_reglament_eur=$("#present_reglament_eur").val();
                            d.filtrar_data_citacions=$("#filtrar_data_citacions").is(":checked");
                            d.data_min_citacio=$("#data_min_citacio").val();
                            d.data_max_citacio=$("#data_max_citacio").val();
//                            d.=$("#").val();
                        }
                    },
                    "deferRender": true,
                    columns:[
                        {'data': 'id'},
                        {'data': 'especie'},
                        { data:{'sinonims':'sinonims'},"render": function(data){
                            if(data['sinonims']==null)
                                return '<a class="btn btn-info disabled"><span class="glyphicon glyphicon-eye-close" aria-hidden="true"><i class="fa fa-eye-slash fa-lg"></i></span></a>';
                            else
                                return '<a class="btn btn-info sinonims_especie" title="'+data['sinonims']+'"><span class="glyphicon glyphicon-eye-open" aria-hidden="true"><i class="fa fa-eye fa-lg"></i></span></a>';
                        }},
                        {'data': 'grup'},
//                        {'data': 'estatuscat'},
//                        {'data': 'varietat'},
//                        {'data': 'regionativa'},
//                        {'data': 'viaentrada'},
//                        {'data': 'estatushistoric'},
//                        {'data': 'present'},
//                        {'data':{'id':'id'},"render": function(data){return '<a class="btn btn-info mostrar_info_especie" value="'+data["id"]+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>';}}
                        {'data':{'id':'id'},"render": function(data){return '<a class="btn btn-success mostrar_info_especie" value="'+data["id"]+'" title="Veure info completa" href="#"><i class="fa fa-info fa-lg"></i> <i class="fa fa-newspaper-o fa-lg"></i></a>';}}
                    ],
                    columnDefs:[
                        {"visible":false,"targets":[0]},
                        { "width": "5%", "targets": [2,4] }
                    ],
                    order: [[ 1, "asc" ]],
//                    fnDrawCallback:function(){// OJO es sensible a mayusculas y minusculas
//                        var total = $(this).DataTable().column( 5 ).data().sum();
//                        $("#total_periodicitat_partida").val(total);
//                    },
                    drawCallback: function(){
                        $(".sinonims_especie").tooltip();
                    },
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    searching:false,
//                    "pagingType": "full_numbers",
//                    paging:         false,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
        // Ojo ESTO SIRVE PARA OBTENER EL JSON DE LA TABLA
        taula_especies.on( 'xhr', function () {
            var json = taula_especies.ajax.json();
            //console.log(json["ids_especies"]);
            $("#ids_especies_filtradas").attr("value",json["ids_especies"]);
            //$("#ids_especies_filtradas").attr("num_elem",json["num_elem"]);
        } );


        taula_especies_map = $("#table_info_map").DataTable({
                    columnDefs:[
                        { "width": "5%", "targets": [8] },
                        { "width": "10%", "targets": [0,1,2,3,4,5,6,7] }
                    ],
                    dom: 'Bfrtip',
                    buttons:[{
                            extend: 'print',
                            header: true,
                            footer: true,
                            title: function(){return "Informació de area geogràfica"},
                            text: '<span aria-hidden="true"><i class="fa fa-print fa-lg"></i> Imprimir</span>',
                            autoPrint: true,
                            exportOptions: {
                                columns: [0,1,2,3,4,5,6,7],
                            }
                    },{
                        extend: 'excel',
                        filename: function(){return  "Informació de area geogràfica"},
                        text: '<span aria-hidden="true"><i class="fa fa-file-excel-o fa-lg"></i> Excel</span>',
                        exportOptions: {
                            columns: ':visible',
                        }
                    },{
                        extend: 'pdf',
                        title: function(){return  "Informació de area geogràfica"},
                        text: '<span aria-hidden="true"><i class="fa fa-file-pdf-o fa-lg"></i> PDF</span>',
                        exportOptions: {
                            columns: [0,1,2,3,4,5,6,7],
                        }
                    },{
                        extend: 'csv',
                        filename: function(){return  "Informació de area geogràfica"},
                        text: '<span aria-hidden="true"><i class="fa fa-table fa-lg"></i> CSV</span>',
                        exportOptions: {
                            columns: [0,1,2,3,4,5,6,7],
                        }
                    }],
                    order: [[ 0, "asc" ]],
                    scrollY:        '50vh',
                    scrollCollapse: true,
                    searching:false,
                    autowidth:      true,
                    overflow:       "auto",
                    paging: false,
                    language: opciones_idioma,
        });

        /// RESUM DE LOCALITATS
        taula_resum_localitats_especie = $("#table_resum_localitats_especie").DataTable({
                    columnDefs:[
                        { "width": "20%", "targets": [0] }
                    ],
                    dom: 'Bfrtip',
                    buttons:[{
                            extend: 'print',
                            header: true,
                            footer: true,
                            title: function(){return '<h4>Resum de localitats de <b>'+taula_resum_localitats_especie.cell(0,1).data()+'</b></h4>'},
                            text: '<span aria-hidden="true"><i class="fa fa-print fa-lg"></i> Imprimir</span>',
                            autoPrint: true
                    },{
                        extend: 'excel',
                        filename: function(){return 'Resum de localitats de '+taula_resum_localitats_especie.cell(0,1).data()},
                        text: '<span aria-hidden="true"><i class="fa fa-file-excel-o fa-lg"></i> Excel</span>',
                    },{
                        extend: 'pdf',
                        title: function(){return 'Resum de localitats de '+taula_resum_localitats_especie.cell(0,1).data()},
                        text: '<span aria-hidden="true"><i class="fa fa-file-pdf-o fa-lg"></i> PDF</span>'
                    },{
                        extend: 'csv',
                        filename: function(){return 'Resum de localitats de '+taula_resum_localitats_especie.cell(0,1).data()},
                        text: '<span aria-hidden="true"><i class="fa fa-table fa-lg"></i> CSV</span>'
                    },{
                        text: '<span aria-hidden="true"><i class="fa fa-file-text-o fa-lg"></i>CSV amb detalls de UTMs</span>',
                        className: 'text-success',
                        action: function (){
                            $("#form_generar_csv_citacions_detalls").submit();
                            alert("Generant l'arxiu...");
                        }
                    }],
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
        ////////////////////////
        /// DOCUMENTACIO ESPECIE
        taula_documentacio_especie = $("#table_documentacio_especie").DataTable({
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

        ////////////////////////

        /// ACTUACIONS DE CONTROL
        taula_actuacions_especie = $("#table_actuacions_especie").DataTable({
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

        ////////////////////////

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
            taula_especies.page( 'first' );
            event.preventDefault();
            taula_especies.ajax.url("/ajax_taula_especies_filtres/");
            taula_especies.ajax.reload(null,false);
            //console.debug(event);
        });

        $('.buscar_per').on( 'click', function () {
            if($(this).val()==1){
                $("#div_buscar_taxon").show();
                $("#div_buscar_sinonim").hide();
            }else{
                $("#div_buscar_taxon").hide();
                $("#div_buscar_sinonim").show();
            }
        } );

        // GENERAR CSV
        $("#generar_csv").click(function(){

            $("#form_generar_csv").submit();
//              $.ajax({
//                type: "POST",
//                url: "/generar_csv_especies/",
//                data: {"ids":$("#ids_especies_filtradas").attr("value")},
//                sucess:function(response, status, request){
//                    console.log(response);
//                    alert("exito");
//                }
//              });

//            var num = parseInt($("#ids_especies_filtradas").attr("num_elem"));
//            if(num > 100){
//                $.confirm({
//                    title: 'Alerta',
//                    content: "Es mostraran les dades de més de 100 espècies ("+num+"). Això podria fer que la generació del document trigui una mica.",
//                    confirmButton: 'Endavant',
//                    cancelButton: 'Cancel·lar',
//                    confirmButtonClass: 'btn-info',
//                    cancelButtonClass: 'btn-danger',
//                    closeIcon: false,
//                    confirm: function(){
//                        window.open("/generar_csv_especies/"+$("#ids_especies_filtradas").attr("value"));
//                    },
//                    cancel: function(){
//                    }
//                });
//            }
//            else{
                //window.open("/generar_csv_especies/"+$("#ids_especies_filtradas").attr("value"));
//            }


        });

        // GENERAR CSV CON INFORME DE ESPECIES Y CITACIONES DE CADA UTM 10KM(EL BOTON ESTA EN AREES GEOGRAFIQUES)
        $("#boton_informe_utm10").click(function(){

            $("#form_generar_csv_informe_utm10").submit();
        });

         //GENERAR INFORME CSV CON ESPECIES Y TODAS LAS UTMS10KM DONDE HA SIDO ENCONTRADA(TAMBIEN SE CUENTAN COMO UTMS10 AQUELLAS QUE TENGAN UNA DE 1KM O UNA CITACION DENTRO)(EL BOTON ESTA EN AREES GEOGRAFIQUES)
        $("#boton_informe_especies_utm10").click(function(){

            $("#form_generar_csv_informe_especies_utm10").submit();
        });


        // ajustar columnas al cargar un tab
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();
        });

        // Limpiar filtros
        $("#limpiar_filtros").on("click",function(){
            limpiar_filtros();
        });

        //tooltip de las herramientas
        $(".boton_herramientas").tooltip();
        $(".boton_tooltip").tooltip();
});
function comprobar_filtrar_data_citacio(){
    if($("#filtrar_data_citacions").is(":checked")){
        //$("#data_min_citacio").val("");
        $("#data_min_citacio").attr("disabled",false);
        //$("#data_max_citacio").val("");
        $("#data_max_citacio").attr("disabled",false);
    }else{
        $("#data_min_citacio").val("");
        $("#data_min_citacio").attr("disabled",true);
        $("#data_max_citacio").val("");
        $("#data_max_citacio").attr("disabled",true);
    }
}

function comprobar_buscar_per(){
    if($("input:radio[name='buscar_per']:checked").val()==1){
        $("#div_buscar_taxon").show();
        $("#div_buscar_sinonim").hide();
    }else{
        $("#div_buscar_taxon").hide();
        $("#div_buscar_sinonim").show();
    }
}
function limpiar_filtros(){
    $("#form_filtres .form-control").each(function(){
        $(this).val($(this).data("original-value"));
    });
    $("#filtrar_data_citacions").prop("checked",false);
    comprobar_filtrar_data_citacio();
}

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
            this.grup,
            this.estatus_cat,
            this.nutm10000,
            this.nutm1000,
            this.ncitacions,
            this.nmassesaigua,
            total,
//            this.nutms10totals,
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
            this.grup,
            this.estatus_cat,
            this.nutm10000,
            this.nutm1000,
            this.ncitacions,
            this.nmassesaigua,
            total,
//            this.nutms10totals,
            '<a class="btn btn-info mostrar_info_especie" value="'+this.id+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>'
        ]);
    });
    taula_especies_map.draw();
}

function rellenar_table_resum_localitats_especie(data){ // esta funcion se llama en info_especie.js
    //taula_resum_localitats_especie.columns(0).clear();
    //taula_resum_localitats_especie.cell(0,1).data(data["genere"]+" "+data["especie"]);
    //taula_resum_localitats_especie.cell(1,1).data(data["grup"]);
    taula_resum_localitats_especie.cell(0,1).data(data["nom_especie"]);
    taula_resum_localitats_especie.cell(1,1).data(data["estatus_cat"]);
    taula_resum_localitats_especie.cell(1,1).data(data["nutm10000"]);
    taula_resum_localitats_especie.cell(2,1).data(data["nutm1000"]);
    taula_resum_localitats_especie.cell(3,1).data(data["ncitacions"]);
    taula_resum_localitats_especie.cell(4,1).data(data["nmassesaigua"]+data["nmassesaigua_identificades"]);
    taula_resum_localitats_especie.cell(5,1).data(data["nutm10000"]+data["nutm1000"]+data["ncitacions"]+data["nmassesaigua"]);
    $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();///IMPORTANTE sirve para alinear correctamente las cabezeras de las datatables,ya que con divs que estan hidden no se alineaban automaticamente
//    $(data["citacions"]).each(function(){
//
//    });
}

function rellenar_table_documentacio_especie(data){ // esta funcion se llama en info_espcie,js
    taula_documentacio_especie.clear();
    $(data).each(function(){
//                console.log(this);
        taula_documentacio_especie.row.add([
            this.titol,
            '<a class="btn btn-info mostrar_info_especie" target="_blank" title="Obrir arxiu" href="'+this.fitxer+'"><i class="fa fa-file fa-lg"></i></a>'
        ]);
    });
    taula_documentacio_especie.draw();
}


function rellenar_table_actuacions_especie(data){ // esta funcion se llama en info_espcie,js
    taula_actuacions_especie.clear();
    $(data).each(function(){
//                console.log(this);
        taula_actuacions_especie.row.add([
            this.titol,
            '<a class="btn btn-info mostrar_info_especie" target="_blank" title="Obrir arxiu" href="'+this.fitxer+'"><i class="fa fa-file fa-lg"></i></a>'
        ]);
    });
    taula_actuacions_especie.draw();
}

function descargar_csv(url){
    data = {
        ids: $("#ids_especies_filtradas").attr("value"),
        csrfmiddlewaretoken:'{{ csrf_token }}'

    };

    // Use XMLHttpRequest instead of Jquery $ajax
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        var a;
        if (xhttp.readyState === 4 && xhttp.status === 200) {
            // Trick for making downloadable link
            a = document.createElement('a');
            a.href = window.URL.createObjectURL(xhttp.response);
            // Give filename you wish to download
            a.download = "test-file.xls";
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
        }
    };
    // Post data to URL which handles post request
    xhttp.open("POST", url);
    xhttp.setRequestHeader("Content-Type", "application/json");
    // You should set responseType as blob for binary responses
    xhttp.responseType = 'blob';
    xhttp.send(JSON.stringify(data));
}
//function ajustar_columnas_actual_tab(){
//    $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();
//}


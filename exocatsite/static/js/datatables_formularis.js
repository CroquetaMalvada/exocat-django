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

var taula_formularis_usuari;
$(document).ready(function(){

    // Si se esta cargando especies:


    taula_formularis_usuari = $("#taula_formularis_usuari").DataTable({
//                    processing:true,
//                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                    ajax: {
                        url: '/ajax_formularis_usuari/',
                        dataSrc: '',
                    },
                    "deferRender": true,
                    columns:[
                        {'data': 'id'},
                        {'data': 'especie'},
                        {'data': 'usuari'},
                        {'data': 'validat'},
                        {'data':{'id':'id'},"render": function(data){return '<a class="btn btn-info editar_formulari" value="'+data["id"]+'" title="Info" href="#"><i class="fa fa-edit fa-lg"></i></a>';}}
//                        {'data':{'id':'id'},"render": function(data){return '<form action="/formularis_localitats_especie/" method="get"><input value="'+data["id"]+'" hidden/><button class="btn btn-info" title="EDITAR FORMULARI"><i class="fa fa-eye fa-lg"></i></form>';}}
                    ],
                    columnDefs:[
//                        {"visible":false,"targets":[0]},
                        { "width": "5%", "targets": [0,3] }
                    ],
                    order: [[ 1, "asc" ]],
                    scrollY:        '80vh',
                    scrollCollapse: true,
                    searching:true,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
        // ajustar columnas al cargar un tab
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();
        })

        $("#taula_formularis_usuari").on( 'click', '.editar_formulari', function (){
            $("#id_form").val($(this).attr("value"));
            $("#form_formularis_usuari").trigger("submit");
        });
});
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

var taula_revisar_citacions_aca;
var especies_autocomplete;
var id_citacio_revisar;

$(document).on( 'click','.btn_revisar_citacio_aca', function (e) {
    id_citacio_revisar=$(this).attr("value");
    $("#dialogrevisar_citacio").dialog("open");
    $("#nom_de_especie").html($(this).attr("nom"));
});
$(document).on( 'click','#revisar_especie', function (e) {
    revision_especie($('#especies_autocomplete').attr("valor"));
});


$(document).ready(function(){

    // Si se esta cargando especies:

    $.fn.dataTable.moment( 'DD-MM-YYYY' ); ///para definir el formato estandar de fechas en las tables(depende de datetime-moment.js y moment.min.js)
    taula_revisar_citacions_aca = $("#taula_citacions_revisar").DataTable({
//                    processing:true,
//                    serverSide:true,
//                    ajax: '/ajax_taula_especies/',
//                    deferLoading: 10,
                    ajax: {
                        url: '/ajax_revisar_citacions_aca/',
                        dataSrc: '',
                    },
                    "deferRender": true,
                    columns:[
                        {'data': 'nom'},
                        {'data': 'data'},
                        {'data':{'revisat':'revisat'},"render": function(data){
                            if (data["revisat"]==0)
                                return "No";
                            else
                                return "Si";
                        }},
                        {'data':{'id':'id','nom':'nom'},"render": function(data){return '<a class="btn btn-info btn_revisar_citacio_aca" value="'+data["id"]+'" nom="'+data["nom"]+'" title="Revisar" href="#"><i class="fa fa-edit fa-lg"></i></a>';}}
//                        {'data':{'id':'id'},"render": function(data){return '<form action="/formularis_localitats_especie/" method="get"><input value="'+data["id"]+'" hidden/><button class="btn btn-info" title="EDITAR FORMULARI"><i class="fa fa-eye fa-lg"></i></form>';}}
                    ],
                    columnDefs:[
//                        {"visible":false,"targets":[0]},
                        { "width": "5%", "targets": [2,3] }
                    ],
                    createdRow:function(row, data, dataIndex){
                        // color de celda
                            //alert(data["revisat"]);
                        if(data["revisat"]==0){
                            $(row).css({"background-color":"LightCoral"});
                        }else{
                            $(row).css({"background-color":"LightGreen"});
                        }
                    },
                    order: [[ 1, "asc" ]],
                    scrollY:        '80vh',
                    scrollCollapse: true,
                    searching:true,
                    autowidth:      true,
                    overflow:       "auto",
                    language: opciones_idioma,
        });
        //console.log(especies_autocomplete);
        /// habilitar el autocompletar
        $( "#especies_autocomplete" ).autocomplete({
            minLength: 2,
//            autoFocus: true,
//            appendTo: "#dialogrevisar_citacio",
            "source": especies_autocomplete,
            "select": function (event, ui) { ///CUANDO EL USUARIO ELIJA UNA OPCION,EL VALOR VERDADERO SE ESCONDERA
                // Set autocomplete element to display the label
                this.value = ui.item.label;
                // Store value in hidden field
                $('#especies_autocomplete').attr("valor",ui.item.value);

                // Prevent default behaviour
                return false;
            },
            "create": function (event, ui) {
                $('#especies_autocomplete')[0].value = ""; // Clear the input field
            }
        });
        //$('#especies_autocomplete').data().autocomplete.term = null;

        // ajustar columnas al cargar un tab
        $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
            $.fn.dataTable.tables( {visible: false, api: true} ).columns.adjust().draw();
        })

        $("#taula_formularis_usuari").on( 'click', '.editar_formulari', function (){
            $("#id_form").val($(this).attr("value"));
            $("#form_formularis_usuari").trigger("submit");
        });

        /////DIALOG
        $("#dialogrevisar_citacio").dialog({
            modal:true,
            resizable:true,
            draggable:true,
            width: '50%',
            closeOnEscape:true,
            autoOpen:false,
            show: {effect:"puff", duration:500},
            hide: {effect:"puff", duration:500},
            close: function(){
                $('#especies_autocomplete')[0].value = ""; // Reiniciar el valor del input de especies
            }
    //        content:$("#dialogdiv"),
        });
});

function revision_especie(id_exo){
    $.ajax({
        dataType: "json",
        url: "/revisar_citacio_especie_aca/",
        method: "POST", //<-- Necesario el token_ajax.js
        data: {"id":id_citacio_revisar,"id_especie_exocat":id_exo},
        success: function(data) {
            alert("Canvis guardats amb èxit.");
            taula_revisar_citacions_aca.ajax.reload();
//            $("#foto_principal_gallery").append(
//              "<img width='200' src='" + data.url + "'></img>  <br>"
//            );
        },
        error: function(data){
//           alert(data.status); // the status code
           alert(data.responseJSON.error); // the message
        },
        complete:function(){
            $("#dialogrevisar_citacio").dialog("close");
        }
    });
}
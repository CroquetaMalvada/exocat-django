$(document).ready(function(){
    //descolutamos el informe y lo ocultamos con la funcion
    $("#informe_colgar_fichero").removeAttr("hidden");
    mostrar_instrucciones();


    $("#descargar_plantilla_1").click(function(){
        $("#tipo").attr("value",1);
        $("#form_generar_csv_plantilla_citaciones").submit();
    });
    $("#descargar_plantilla_2").click(function(){
        $("#tipo").attr("value",2);
        $("#form_generar_csv_plantilla_citaciones").submit();
    });
    $("#boton_colgar_csv_citaciones").click(function(){
        $("#colgar_csv_citaciones").click();
    });
    $("#colgar_csv_citaciones").change(function(){
        $("#form_colgar_csv_citaciones").submit();
    });

    $("#form_colgar_csv_citaciones").on("submit",function(e){
        e.preventDefault();
        var datos= new FormData(document.getElementById("form_colgar_csv_citaciones"));
        datos.append("csrfmiddlewaretoken",$("#colgar_csv_citaciones").attr("token"));
        $.ajax({
            url:"/upload_citaciones_csv/",
            type:"POST",
            dataType:"json",
            data:datos,
            cache:false,
            contentType: false,
            processData:false,
            success:function(data){
                //alert(data["errores"]);
                console.log(data);
                if(data["errores"]>0){
                    alert("Error al pujar l'arxiu. Es motrarà l'informe d'errors a continuació.");
                    $("#lista_errores").html("");
                    $.each(data["listado_errores"],function(index,error){
                        $("#lista_errores").append(
                            '<div class="alert alert-danger"><i class="fa fa-exclamation-triangle" style="color:orange"></i>'+error+'</div>'
                        );
                    })
                    mostrar_informe();
                }
                //alert("hola");

                //console.log("hola");
            },
            error:function(){
                alert("Error");
            }
        });
    });

//    $('#colgar_csv_citaciones').fileupload({
//        dataType: 'json',
//        done: function (e, data) {
//            $.each(data.result.files, function (index, file) {
//                $('<p/>').text(file.name).appendTo(document.body);
//            });
//        }
//    });
});
function mostrar_instrucciones(){
    $("#informe_colgar_fichero").hide();
    $("#contenedor_instrucciones_fichero").show();
}
function mostrar_informe(){
    $("#contenedor_instrucciones_fichero").hide();
    $("#informe_colgar_fichero").show();
}
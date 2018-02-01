$(document).ready(function(){

    $(".opcion_cabecera").click(function(){
        var mostrar="";
        if($(this).attr("id")=="cabecera_llistat_especies")
            mostrar="llistat_especies_div";
        else if($(this).attr("id")=="cabecera_mapa")
            mostrar="div_mapa";


        $(".contenido").each(function(){
            //alert($(this).attr("id")+" - "+mostrar);
            if($(this).attr("id")==mostrar)
                $(this).show();
            else
                $(this).hide();
//            if($(evt).attr("id")=="cabecera_llistat_especies")
//                $("#llistat_especies_div").show();
//            else if($(evt).attr("id")=="cabecera_mapa")
//                $("#div_mapa").show();
//            alert($(this).attr("id");
        });
    });
});
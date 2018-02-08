$(document).ready(function(){
    $(".opcion_cabecera").click(function(){
        var mostrar="";
        if($(this).attr("id")=="cabecera_llistat_especies")
            mostrar="llistat_especies_div";
        else if($(this).attr("id")=="cabecera_mapa"){
            mostrar="div_mapa";
            if(taula_especies_map.data().any()) // si la tabla esta vacía las columnas quedan raras,asi que ponemos este if
                taula_especies_map.clear().draw();
        }else if($(this).attr("id")=="cabecera_colaboradors")
            mostrar="div_colaboradors";
        else if($(this).attr("id")=="cabecera_coordinacio")
            mostrar="div_coordinacio";
        mostrar_contenido(mostrar);
    });
    mymap.invalidateSize(false);
    mostrar_contenido("llistat_especies_div");
});

function mostrar_contenido(mostrar){
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
}
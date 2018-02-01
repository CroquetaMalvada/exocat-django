$(document).on( 'click','.mostrar_info_especie', function (e) {
    resetear_nav();
    $("#mapa_de_especie").attr("value",$(this).attr("value"));

    $.ajax({
        dataType: "json",
        url: '/ajax_mostrar_info_especies/',
        method: 'POST',
        data: {"id":$(this).attr("value")},

        success: function(data){

            $('#info_genere').html(data['genere']);
            $('#info_especie').html(data['especie']);
            $('#info_subespecie').html(data['subespecie']);
            $('#info_varietat').html(data['varietat']);
            $('#info_subvarietat').html(data['subvarietat']);
            $('#info_nomsvuglars').html(data['nomsvulgars']);
            $('#info_grup').html(data['grup']);
            $('#info_regionativa').html(data['regionativa']);
            $('#info_estatushistoric').html(data['estatushistoric']);
            $('#info_estatuscatalunya').html(data['estatuscatalunya']);
            $('#info_viesentrada').html(data['viesentrada']);
            $('#info_presentcatalog').html(data['presentcatalog']);
            $('#info_observacions').html(data['observacions']);
            $('#info_titolimatge').html(data['titolimatge']);

            //imagen principal
            $("#info_imatge").attr("src","http://montesdata.creaf.cat/Exocat/grafics_temp/"+data['id']+"_port.jpg");
            $("#info_imatge").attr("title",data['titolimatge']);


            $("#carousel_contenido").html("");

            $.each(data["imatges"],function(k,v){
                var titulo = String(this["titol"]);
                titulo=titulo.replace(/"/g,"'"); //quitamos todas las comillas dobles para evitar problemas

                var html='<div class="carousel-item"><img style="padding:10%"title="'+titulo+'" class="d-block img-fluid" width="100%" src="http://montesdata.creaf.cat/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'" alt="http://montesdata.creaf.cat/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'" /><div class="carousel-caption d-none d-md-block"><p><a class="btn btn-success" href="http://montesdata.creaf.cat/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'"><i class="fa fa-search-plus"></i> Ampliar</a></p></div</div>';
                $("#carousel_contenido").append(html);
            });

            $('.carousel-item').first().addClass('active');//si es la priemra imagen la ponemos como activa
            $("#info_titolimatge").html($(".active img").attr("title"));
            $("#info_imatges").carousel();

            //        $('#info_').html(data['']);

            //        $("#info_observacions").tooltip(); !mejor no usar este tooltip y mostrar la info bajo la imagen para que la gente no tenga que usar el cursor
            $("#dialogdiv").dialog("open");

        }

    });

});

//cuando una imagen del carosuel cambia,lo hace tambien su texto inferior
$(document).on('slid.bs.carousel', function () {
        $("#info_titolimatge").html($(".active > img").attr("title"));
});




$(document).ready(function(){

    dialoginfo=$("#dialogdiv").dialog({
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
//dialoginfo.dialog("open");


});

function resetear_nav(){
$(".nav-link").removeClass("active");
$(".tab-pane").removeClass("active");
$("#navlink_dades_basiques").tab("show")
//$("#div_dades_basiques").addClass("active")
}

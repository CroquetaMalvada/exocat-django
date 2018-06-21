$(document).on( 'click','.mostrar_info_especie', function (e) {
    resetear_nav();
    $("#mapa_de_especie").attr("value",$(this).attr("value"));
    $.ajax({
        dataType: "json",
        url: '/ajax_mostrar_info_especies/',
        method: 'POST',
        data: {"id":$(this).attr("value")},

        success: function(data){
            var nombre = data['genere']+"_"+data['especie'];
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
            $('#info_presenteuropeu').html(data['presentreglamenteur']);
            //

            if(data['observacions'].length>100){
                $('#info_observacions').html(data['observacions'].substring(0,100)+"...");
            }else{
                $('#info_observacions').html(data['observacions']);
            }
            $('#observaciones_tooltip').attr("title",data['observacions']);
            $("#observaciones_tooltip").tooltip();
            //
            $('#info_titolimatge').html(data['titolimatge']);

            //ocultar la info vacia
            $(".dada_especie").each(function(){
                if($(this).html()==""){
                    $(this).parent("p").hide();
                    $(this).parent("p").next("hr").hide();
                }else{
                    $(this).parent("p").show();
                    $(this).parent("p").next("hr").show();
                }
            });
            /////
            //// ICONOS PARA EXPORTAR LAS LAYERS
            $("#exportar_presencia_10000").empty();
            $("#exportar_presencia_1000").empty();
            $("#exportar_presencia_citacions").empty();
            $("#exportar_presencia_masses").empty();
            var icons_pres_10000="   [ZIP - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:PRESENCIA_SP_10000_p&outputFormat=SHAPE-ZIP&format_options=filename:"+nombre+"_UTM10km.zip&CQL_FILTER=IDSPINVASORA%3D%27"+data['id']+"%27' title='Exportar WFS' id='exportar_wfs_presencia_10000'><i class='fa fa-file-zip-o fa-lg'></i></a>]   [KML - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:PRESENCIA_SP_10000_p&outputFormat=application/vnd.google-earth.kml+xml&format_options=filename:"+nombre+"_UTM10km&CQL_FILTER=IDSPINVASORA%3D%27"+data['id']+"%27' title='Exportar kml' id='exportar_wms_presencia_10000'><i class='fa fa-globe fa-lg'></i></a>]"
            var icons_pres_1000="   [ZIP - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:PRESENCIA_SP_1000_p&outputFormat=SHAPE-ZIP&format_options=filename:"+nombre+"_UTM1km.zip&CQL_FILTER=IDSPINVASORA%3D%27"+data['id']+"%27' title='Exportar WFS' id='exportar_wfs_presencia_10000'><i class='fa fa-file-zip-o fa-lg'></i></a>]   [KML - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:PRESENCIA_SP_1000_ps&outputFormat=application/vnd.google-earth.kml+xml&format_options=filename:"+nombre+"_UTM1km&CQL_FILTER=IDSPINVASORA%3D%27"+data['id']+"%27' title='Exportar kml' id='exportar_wms_presencia_1000'><i class='fa fa-globe fa-lg'></i></a>]"
            var icons_pres_citacions="   [ZIP - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:citacions&outputFormat=SHAPE-ZIP&format_options=filename:"+nombre+"_citacions.zip&CQL_FILTER=idspinvasora%3D%27"+data['id']+"%27' title='Exportar WFS' id='exportar_wfs_presencia_10000'><i class='fa fa-file-zip-o fa-lg'></i></a>]   [KML - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:citacions&outputFormat=application/vnd.google-earth.kml+xml&format_options=filename:"+nombre+"_citacions&CQL_FILTER=idspinvasora%3D%27"+data['id']+"%27' title='Exportar kml' id='exportar_wms_citacions'><i class='fa fa-globe fa-lg'></i></a>]"
            // var icons_pres_citacions="   [WFS - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:citacions&outputFormat=SHAPE-ZIP&format_options=filename:"+nombre+"_citacions_WFS.zip&CQL_FILTER=idspinvasora%3D%27"+data['id']+"%27' title='Exportar WFS' id='exportar_wfs_presencia_10000'><i class='fa fa-map fa-lg'></i></a>]   [WMS - <a href='http://exocat2.creaf.cat/geoserver/wms?service=WMS&version=1.1.0&request=GetMap&layers=SIPAN:citacions&styles=&CQL_FILTER=idspinvasora%3D%27"+data['id']+"%27&bbox=246809.50679615702,4429945.3655678565,531814.7343779552,4804968.5619192235&width=389&height=512&srs=EPSG:23031&format=application/vnd.google-earth.kml+xml' title='Exportar WMS' id='exportar_wms_presencia_10000'><i class='fa fa-globe fa-lg'></i></a>]"
            var icons_pres_masses="   [ZIP - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:MASSA_AIGUA&outputFormat=SHAPE-ZIP&format_options=filename:"+nombre+"_masses_aigua.zip&CQL_FILTER=idtaxon%3D%27"+data['id']+"%27' title='Exportar WFS' id='exportar_wfs_presencia_10000'><i class='fa fa-file-zip-o fa-lg'></i></a>]   [KML - <a href='http://exocat2.creaf.cat/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SIPAN:MASSA_AIGUA&outputFormat=application/vnd.google-earth.kml+xml&format_options=filename:"+nombre+"_masses_aigua.kml&CQL_FILTER=idtaxon%3D%27"+data['id']+"%27' title='Exportar kml' id='exportar_wms_masses'><i class='fa fa-globe fa-lg'></i></a>]"
            $("#exportar_presencia_10000").append(icons_pres_10000);
            $("#exportar_presencia_1000").append(icons_pres_1000);
            $("#exportar_presencia_citacions").append(icons_pres_citacions);
            $("#exportar_presencia_masses").append(icons_pres_masses);


            //imagen principal
            //$("#info_imatge").attr("src","http://exocat2.creaf.cat:8080/Exocat/grafics_temp/"+data['id']+"_port.jpg");
            $("#info_imatge").attr("src","");
            $("#sense_imatge_principal").html("");
            if(data['imatges'][0]){
                $("#info_imatge").attr("src","/media/imatges_especies/"+data['imatges'][0]["id"]+".jpg");
            }else{
                $("#info_imatge").attr("src","/media/imatges_especies/no_image.jpg");
                $("#sense_imatge_principal").html("SENSE IMATGE");
            }
            $("#info_imatge").attr("title",data['titolimatge']);


            // resum de localitats(suma de citacions,utms,masses...)
            rellenar_table_resum_localitats_especie(data);

            // documentacio de la especie
            rellenar_table_documentacio_especie(data['documentacio']);

            // actuacions de control
            rellenar_table_actuacions_especie(data['actuacions']);



            $("#carousel_contenido").html("");

            $.each(data["imatges"],function(k,v){
                var titulo = String(this["titol"]);
                titulo=titulo.replace(/"/g,"'"); //quitamos todas las comillas dobles para evitar problemas

                //var html='<div class="carousel-item"><img style="padding:10%"title="'+titulo+'" class="d-block img-fluid" width="100%" src="http://exocat2.creaf.cat:8080/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'" alt="http://exocat2.creaf.cat:8080/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'" /><div class="carousel-caption d-none d-md-block"><p><a class="btn btn-success" href="http://exocat2.creaf.cat:8080/Exocat/media/visualitzarfoto.htm?id='+this["id"]+'"><i class="fa fa-search-plus"></i> Ampliar</a></p></div</div>';
                var html='<div class="carousel-item"><img style="padding:10%"title="'+titulo+'" class="d-block img-fluid" width="100%" src="/media/imatges_especies/'+this["id"]+'.'+this["extensio"]+'"/><div class="carousel-caption d-none d-md-block"><p><a class="btn btn-success" href="/media/imatges_especies/'+this["id"]+'.'+this["extensio"]+'"><i class="fa fa-search-plus"></i> Ampliar</a></p></div</div>';
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

function preparar_informe(){
    var html_boton=$("#boton_informe").html();
    $("#boton_informe").html("<img src='"+$("#filtrar_loading").attr("src")+"'> Generant...");


    //Primero obtenemos las imagenes necesarias
    var url_image="";
    var url_mapa="";
    url_image=$("#info_imatge").prop("src");// OJO importante usar prop para obtener la absoluta
    $('#mapa_de_especie').tab('show');
    leafletImage(map_info_especie, function(err, canvas) {
        getBase64FromImageUrl(url_image,function(data){ //Obtenemos la url en base64 para la imagen y así pasarla en el pdf
            //console.log(data);
            $("#boton_informe").html(html_boton);
            url_image = data;
            //console.log(canvas);
            generar_informe(url_image,canvas.toDataURL("image/png"));
            //window.open(canvas.toDataURL("image/png"), '_blank');
        });
    });
}

//y una vez tenemos las imagenes,creamos el informe
function generar_informe(url_image,url_mapa){
    var cabecera_pdf={text:'Fitxa espècie invasora: '+$("#info_genere").html()+' '+$("#info_especie").html(),style:"titulo"};
    var datos_basicos=[];
    $(".dada_especie").each(function(){
        if($(this).html()!=""){
            datos_basicos.push({text:$(this).prev().text()+$(this).text()});
            datos_basicos.push({canvas: [ { type: 'line', x1: 0, y1: 0, x2: 515, y2: 0, lineWidth: 1 } ]});
            datos_basicos.push({text:" "});
            //{canvas: [ { type: 'line', x1: 0, y1: 0, x2: 515, y2: 0, lineWidth: 1 } ]},
        }
    });
    //alert(url_image);
    var all_pdf = {
        header:cabecera_pdf,
        content: [
            {
                        image: url_image,
                        width: 200,
                        height: 100,
                        style:"titulo"

            },
            {text:" "},
            {text: "Dades bàsiques",style:"header"},
            {text:" "},
            //{image:url_image,width:250,alignment: 'center'},
            {
                columns:[
                    [
                        datos_basicos,
                        //'OBSERVACIONS: '+$("#info_observacions").html(),
                    ]
                ]
            },
            {text:" "},
            {text: "Mapa",style:"header"},
            {text:" "},
            {text:" "},
            {
                columns:[
                    {
                        width: "*",
                        text: "Resum localitats"
                    },{
                        width: "*",
                        text: "Mapa"
                    }
                ]
            },
            {text:" "},
            {
                columns:[
                    {
                        width: "*",
                        table: {
//                            headerRows: 1,
//                            widths: [ '*', 'auto', 100, '*' ],
                            body: [
                              [ 'Espècie', $("#info_genere").html()+' '+$("#info_especie").html() ],
                              [ 'Nº UTMs 10km', $("#td_n_utms_10").text()],
                              [ 'Nº UTMs 1km', $("#td_n_utms_1").text()],
                              [ 'Nº Citacions puntuals', $("#td_n_citacions").text()],
                              [ "Nº Masses d'aigua", $("#td_n_masses").text()],
                              [ { text: 'Localitats Totals:', bold: true }, $("#td_n_localitats_totals").text() ]
                            ]
                        }
                    },{
//                       stack: [/// esto sirve para que se pueda hacer un width con *
//                            {
//                                image: url_mapa,
//                            }
//                       ],
                        image: url_mapa,
                        width: 300,
                        height: 200

                    }

//                    ,[
//                        {image:url_image},
//                        {canvas: [ { type: 'line', x1: 0, y1: 0, x2: 515, y2: 0, lineWidth: 1 } ]},
//                        'OBSERVACIONS: '+$("#info_observacions").html(),
//                        'GÈNERE: '+$("#info_genere").html(),
//                        {canvas: [ { type: 'line', x1: 0, y1: 0, x2: 515, y2: 0, lineWidth: 1 } ]},
//
//                    ]
                ]
            }

        ],
        styles: {
            header: {
            fontSize: 22,
            bold: true
            },
            titulo: {
            italic: true,
            alignment: 'center'
            }
        }
    };

    pdfMake.createPdf(all_pdf).download('Fitxa '+$("#info_genere").html()+' '+$("#info_especie").html()+'.pdf');
//
//    var doc = new jsPDF()
//
//    doc.addHTML($("#div_dades_basiques").html());
//    doc.save('a4.pdf')

//    var contenido_pdf=html2canvas(document.getElementById("div_dades_basiques")).then(function(canvas){
//            var all_pdf = {
//                header:cabecera_pdf,
//                content: [{image:canvas.toDataURL(),width:"auto"}]
//            };
//            pdfMake.createPdf(all_pdf).download('optionalName.pdf');
//    });


//var all_pdf = {
//    header:cabecera_pdf,
//    content: contenido_pdf
//};
//pdfMake.createPdf(all_pdf).download('optionalName.pdf');
}


function getBase64FromImageUrl(url, callback) {
    var img = new Image();

    img.onload = function () {
        var canvas = document.createElement("canvas");
        canvas.width =this.width;
        canvas.height =this.height;

        var ctx = canvas.getContext("2d");
        ctx.drawImage(this, 0, 0);

        var dataURL = canvas.toDataURL("image/png");
        callback(dataURL);
    };

    img.onerror = function() {
      console.warn('error loading' + url);
    };

    img.src = url;
}

//function getBase64FromImageUrl(url) {
//
//
//    var img = new Image();
//
//    img.setAttribute('crossOrigin', 'anonymous');
//
//    img.onload = function () {
//        var canvas = document.createElement("canvas");
//        canvas.width =img.width;
//        canvas.height =img.height;
//
//        var ctx = canvas.getContext("2d");
//        ctx.drawImage(img, 0, 0);
//
//        var dataURL = canvas.toDataURL("image/png");
//
//        alert(dataURL.replace(/^data:image\/(png|jpg);base64,/, ""));
//        return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
//    };
//
////    img.src = url;
////    return url;
//}
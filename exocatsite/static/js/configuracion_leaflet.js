var mymap;
var map_info_especie;
///mapa grande
var wmsLayer_presencia_10000=false;
var wmsLayer_presencia_1000=false;
var wmsLayer_citacions=false;
var wmsLayer_presencia_ma=false;
var wmsLayer_comarques=false;
//mapa info especie
var mapainfo_wmsLayer_presencia_10000=false;
var mapainfo_wmsLayer_presencia_1000=false;
var mapainfo_wmsLayer_citacions=false;
var mapainfo_wmsLayer_presencia_ma=false;

var editableLayers=false;

var modo_info_clicar=false;
var modo_info_comarques=false;

$(document).ready(function(){
    // Google layers
	/*var g_roadmap   = new L.Google('ROADMAP');
	var g_satellite = new L.Google('SATELLITE');
	var g_terrain   = new L.Google('TERRAIN');*/





    var options = {
		container_width 	: "350px",
		container_maxHeight : "500px",
		group_maxHeight     : "100px",
		exclusive       	: false
	};

    //////CONFIG PARA EL MAPA BUENO:
        // OSM layers
        var osmUrl='http://{s}.tile.osm.org/{z}/{x}/{y}.png';
        var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});

        wmsLayer_presencia_10000 = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:PRESENCIA_SP_10000_p',
            transparent: 'true',
            format: 'image/png',
            opacity: 0.5
        });

        wmsLayer_presencia_1000 = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:PRESENCIA_SP_1000_p',
            transparent: 'true',
            format: 'image/png',
            opacity: 0.5
        });

        wmsLayer_citacions = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:citacions',
            transparent: 'true',
            format: 'image/png',
        //        opacity: 0.5
        });

        wmsLayer_presencia_ma = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:presencia_massa_aigua',
            transparent: 'true',
            format: 'image/png',
        //        opacity: 0.5
        });

        wmsLayer_comarques = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:comarques_4326',
            transparent: 'true',
            format: 'image/png',
            opacity: 0.5
        });

        mymap = L.map('map').setView([41.666141,1.761932], 8); //posicion central y zoom por defecto
        ////config para el modulo styledlayercontrol:
        var baseMaps = [
                        /*{
                            groupName : "Google Base Maps",
                            expanded : true,
                            layers    : {
                                "Satellite" :  g_satellite,
                                "Road Map"  :  g_roadmap,
                                "Terreno"   :  g_terrain
                            }
                        },*/
                        {
                            groupName : "Capes base",
                            expanded  : true,
                            layers    : {
                                "OpenStreetMaps" : osm
                            }
                        }
                        /*, {
                            groupName : "Bing Base Maps",
                            layers    : {
                                "Satellite" : bing1,
                                "Road"      : bing2
                            }
                        }*/
        ];

        var overlays = [
                         {
                            groupName : "Presencia espècie",
                            expanded  : true,
                            layers    : {
                                "Presència 10000m" : wmsLayer_presencia_10000,
                                "Presència 1000m" : wmsLayer_presencia_1000,
                                "Citacions" : wmsLayer_citacions,
                                "Masses d'aigua" : wmsLayer_presencia_ma,
                                //"Comarques": wmsLayer_comarques
                            }
                         }
                         /*, {
                            groupName : "Rio de Janeiro",
                            expanded  : true,
                            layers    : {
                                "Bean Plant"     : bean_rj,
                                "Corn Plant" 	 : corn_rj,
                                "Rice Plant"	 : rice_rj
                            }
                         }, {
                            groupName : "Belo Horizonte",
                            layers    : {
                                "Sugar Cane Plant"	: sugar_bh,
                                "Corn Plant" 	 	: corn_bh
                            }
                         }*/
        ];


    //////////////
	var control = L.Control.styledLayerControl(baseMaps, overlays, options);
    mymap.addControl(control);

	////CONFIG PARA EL MAPA DE INFO ESPECIE
	    // OSM layers
        var mapainfo_osmUrl='http://{s}.tile.osm.org/{z}/{x}/{y}.png';
        var mapainfo_osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
        var mapainfo_osm = new L.TileLayer(mapainfo_osmUrl, {attribution: mapainfo_osmAttrib});

        mapainfo_wmsLayer_presencia_10000 = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:PRESENCIA_SP_10000_p',
            transparent: 'true',
            format: 'image/png',
            opacity: 0.5
        });

        mapainfo_wmsLayer_presencia_1000 = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:PRESENCIA_SP_1000_p',
            transparent: 'true',
            format: 'image/png',
            opacity: 0.5
        });

        mapainfo_wmsLayer_citacions = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:citacions',
            transparent: 'true',
            format: 'image/png',
        //        opacity: 0.5
        });

        mapainfo_wmsLayer_presencia_ma = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
            layers: 'SIPAN:presencia_massa_aigua',
            transparent: 'true',
            format: 'image/png',
        //        opacity: 0.5
        });
        map_info_especie = L.map('map_info').setView([41.666141,1.761932], 8);
        ////config para el modulo styledlayercontrol:
        var mapainfo_baseMaps = [
                        /*{
                            groupName : "Google Base Maps",
                            expanded : true,
                            layers    : {
                                "Satellite" :  g_satellite,
                                "Road Map"  :  g_roadmap,
                                "Terreno"   :  g_terrain
                            }
                        },*/
                        {
                            groupName : "Capes base",
                            expanded:true,
                            layers    : {
                                "OpenStreetMaps" : mapainfo_osm
                            }
                        }
                        /*, {
                            groupName : "Bing Base Maps",
                            layers    : {
                                "Satellite" : bing1,
                                "Road"      : bing2
                            }
                        }*/
        ];

        var mapainfo_overlays = [
                         {
                            groupName : "Presencia espècie",
                            expanded  : true,
                            layers    : {
                                "Presència 10000m" : mapainfo_wmsLayer_presencia_10000,
                                "Presència 1000m" : mapainfo_wmsLayer_presencia_1000,
                                "Citacions" : mapainfo_wmsLayer_citacions,
                                "Masses d'aigua" : mapainfo_wmsLayer_presencia_ma,
                            }
                         }
                         /*, {
                            groupName : "Rio de Janeiro",
                            expanded  : true,
                            layers    : {
                                "Bean Plant"     : bean_rj,
                                "Corn Plant" 	 : corn_rj,
                                "Rice Plant"	 : rice_rj
                            }
                         }, {
                            groupName : "Belo Horizonte",
                            layers    : {
                                "Sugar Cane Plant"	: sugar_bh,
                                "Corn Plant" 	 	: corn_bh
                            }
                         }*/
        ];
    //////////////////////
	var control2 = L.Control.styledLayerControl(mapainfo_baseMaps, mapainfo_overlays, options);
	map_info_especie.addControl(control2);

	////

    // MARCAR OPCIONES DE LOS MAPAS
    //en el cuadro de control del mapa bueno seleccionamos la apa del open street map(osm) y la de 10km
	control.selectLayer(osm);
	control.selectLayer(wmsLayer_presencia_10000);

    // en el de la info seleccionamos todas las capas ya que se mostraran las de la especie
	control2.selectLayer(mapainfo_osm);
	control2.selectLayer(mapainfo_wmsLayer_presencia_10000);
	control2.selectLayer(mapainfo_wmsLayer_presencia_1000);
	control2.selectLayer(mapainfo_wmsLayer_citacions);
	control2.selectLayer(mapainfo_wmsLayer_presencia_ma);
	//control.selectLayer(wmsLayer_presencia_10000);

    /////////////////////


//    control2.selectLayer(osm);
//	control2.selectLayer(wmsLayer_presencia_10000);

	//wmsLayer_presencia_10000.setParams({cql_filter:"IDSPINVASORA='Abie_pins'"});
    // create the tile layer with correct attribution




/*
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
    mymap.addLayer(osm);*/
//    mymap.invalidateSize(false);
//    mymap.addLayer(wmsLayer_presencia_10000);
//    mymap.addLayer(wmsLayer_citacions);
//    mymap.addLayer(wmsLayer_presencia_ma);



//STYLED LAYER CONTROL (PARA CLICAR)
//var showGetFeatureInfo = function (err, latlng, content) {
//    //if (err) { console.log(err); return; }
//    // do nothing if there's an error
//    // Otherwise show the content in a popup, or something.
//    L.popup({ maxWidth: 800}).setLatLng(latlng).setContent(content).openOn(mymap);
//};

//var getFeatureInfo = function(evt,querylayers){
//    // Make an AJAX request to the server and hope for the best
//    var url = getFeatureInfoUrl(evt.latlng,querylayers);
//    alert(url);
//    $.ajax({
//        url: url,
//        //type:'json',
//        success: function (data, status, xhr) {
//            console.log(data);
//            var err = typeof data === 'string' ? null : data;
//            if(err){
//                alert("error");
//            }else{
//
//            }
//
//            //showGetFeatureInfo(err, evt.latlng, data);
//        },
//        error: function (xhr, status, error) {
//            alert("error");
//            //showGetFeatureInfo(error);
//        }
//    });
//};

//var getFeatureInfoUrl = function(latlng,querylayers){
//    var point = mymap.latLngToContainerPoint(latlng, mymap.getZoom());
//    var size = mymap.getSize();
//
//    var params = {
//        request: 'GetFeatureInfo',
//        service: 'WMS',
//        srs: 'EPSG:4326',
//        styles: '',
//        transparent: true,
//        version: '1.1.1',
//        format: 'image/jpeg',
//        bbox: mymap.getBounds().toBBoxString(),
//        height: size.y,
//        width: size.x,
//        layers: querylayers,
//        query_layers: querylayers,
//        info_format: 'application/json',
//        feature_count: 100000000
//    };
//
//    params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
//    params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;
//
//    wms_url = "http://montesdata.creaf.cat/geoserver/wms";
////    alert(params.bbox);
////    alert(L.Util.getParamString(params, wms_url, true));
//    return wms_url + L.Util.getParamString(params, wms_url, true);
//};

mymap.on('click', function(evt){
//    if(!$(this).is(".leaflet-draw-section")){
        if(modo_info_clicar){
            limpiar_mapa();
            activar_modo_clicar();

//            var caja=mymap.getBounds().toBBoxString();
//            var punto=mymap.latLngToContainerPoint([wmsLayer_presencia_10000].wmsParams.layers, mymap.getZoom());
//            alert("Lat, Lon : " + evt.latlng.lat + ", " + evt.latlng.lng);

//            $.ajax({
//                url: "/especies_pos/",
//                data:{"lat":evt.latlng.lat,"long":evt.latlng.lng}
//            });

//OJO DESCOMENTAR ESTO SI NO SE LOGRA OBTENER LOS VALROES AL CLICAR!!!!
            obtener_especies_pos(evt.latlng);
//            var layers_in_control = [];
//            layers_in_control.push(wmsLayer_presencia_10000);
////            layers_in_control.push(wmsLayer_presencia_1000);
//            if(layers_in_control.length > 0){
//                var param_layers = [];
//                for(var i=0; i < layers_in_control.length; i++){
//                    param_layers.push( layers_in_control[i].wmsParams.layers );
//                }
//                var querylayers = param_layers.join(',');
//                getFeatureInfo(evt,querylayers);
//            }
        }else if(modo_info_comarques){
            limpiar_mapa();
            activar_modo_clicar_comarques();
            obtener_especies_comarca(evt.latlng);
        }
//    }

});

//////////////////////////////////

//LEAFLET DRAW

editableLayers = new L.FeatureGroup();
mymap.addLayer(editableLayers);



var draw_options = {
    position: 'topleft',
    draw: {
        /*polyline: {
            shapeOptions: {
                color: '#f357a1',
                weight: 10
            }
        },*/
        polyline: false,
        polygon: {
            allowIntersection: false, // Restricts shapes to simple polygons
            drawError: {
                color: '#e1e100', // Color the shape will turn when intersects
                message: '<strong>Error:<strong> No pots dibuixar això.' // Message that will show when intersect
            },
            shapeOptions: {
                color: '#bada55'
            }
        },
        circle: false, // Turns off this drawing tool
        rectangle: {
            shapeOptions: {
                clickable: false
            }
        },
//        marker: {
//            icon: new MyCustomMarker()
//        },
        marker: false,
        circlemarker: false
    }
//    edit: {
//        featureGroup: editableLayers, //REQUIRED!!
//        remove: false
//    }
};


var drawControl = new L.Control.Draw(draw_options);
mymap.addControl(drawControl);

mymap.on(L.Draw.Event.CREATED, function (e) {
    var type = e.layerType,
        layer = e.layer;

//    if (type === 'marker') {
//        layer.bindPopup('A popup!');
//    }
//    console.log(layer.getLatLngs());
//    editableLayers.removeLayer(layer);
//    console.log(layer);
//    mymap.clearLayers(editableLayers);
    limpiar_mapa();
    editableLayers.addLayer(layer);

//    obtener_especies_pos(null,2);// el lanleng que se deberia pasar es un punto de google maps asi que no sirve con una box
    obtener_especies_geom();
});
//////////////////////////////////


/// CUADRO PARA HABILITAR EL CLICAR (el ! del href sirve como preventdefault para evitar el scroll de la pagina al clicar el enlace)
$(".leaflet-draw-toolbar:first").append('<a href="#!" id="boton_info_clicar" onclick="" style="background-image:none;" title="Obtenir info al clicar"><i class="fa fa-crosshairs fa-lg"></i></a>');//<span class="sr-only">Draw a rectangle</span><

/// CUADRO PARA HABILITAR EL CLICAR COMARCAS
$(".leaflet-draw-toolbar:first").append('<a href="#!" id="boton_info_comarques" onclick="" style="background-image:none;" title="Obtenir info sobre una comarca"><i class="fa fa-globe fa-lg"></i></a>');

/// CUANDO SE CLICAN LAS OPCIONES
$(".leaflet-draw-toolbar:first a").on("click",function(evt){
    // si ya esta en modo clicar o comarcas,desactivalos
    limpiar_mapa();
    mymap.addLayer(wmsLayer_presencia_10000);
    if(modo_info_clicar)
        activar_modo_clicar();
    if(modo_info_comarques)
        activar_modo_clicar_comarques();


    // y ahora comprueba si hay que activarlos
    if($(this).attr("id")=="boton_info_clicar"){
        activar_modo_clicar();
    }else if($(this).attr("id")=="boton_info_comarques"){
        activar_modo_clicar_comarques();
    }

});
/// MOVER EL PANEL A LA IZQUIERDA
mover_panel(drawControl.getContainer());


});

function mover_panel(objeto_html){//movemos el panel de control de leaflet al div cerca del mapa
    var div2 = document.getElementById("eines_map");
    div2.appendChild(objeto_html);
}
function activar_modo_clicar(){
    if(modo_info_clicar){
        $("#boton_info_clicar").css("background-color","");
        modo_info_clicar=false;
//        mymap.removeLayer(wmsLayer_presencia_10000);
  //      mymap.removeLayer(wmsLayer_comarques);
        $('.leaflet-container').css( 'cursor', '' );
    }else{
        //mostramos todos los cuadros(haciendo un intersects con un cuadro enorme)
//        mymap.addLayer(wmsLayer_presencia_10000);
        wmsLayer_presencia_10000.setParams({cql_filter:'INTERSECTS(geom_4326,POLYGON((-1.590088 39.736762,-1.590088 43.409038,4.749023 43.409038,4.749023 39.736762,-1.590088 39.736762)))'}) //obtenemos todas las utm de 10km
        $("#boton_info_clicar").css("background-color","lightgreen");
        modo_info_clicar=true;
        $(".leaflet-container").css( 'cursor', 'crosshair' );
    }
}

function activar_modo_clicar_comarques(){
    if(modo_info_comarques){
        $("#boton_info_comarques").css("background-color","");
        modo_info_comarques=false;
        mymap.removeLayer(wmsLayer_comarques);

        $('.leaflet-container').css( 'cursor', '' );
    }else{
        //mostramos todas las comarcas
        //wmsLayer_presencia_10000.setParams({cql_filter:'INTERSECTS(geom_4326,POLYGON((-1.590088 39.736762,-1.590088 43.409038,4.749023 43.409038,4.749023 39.736762,-1.590088 39.736762)))'}) //obtenemos todas las utm de 10km
        mymap.addLayer(wmsLayer_comarques);
        mymap.removeLayer(wmsLayer_presencia_10000);
        $("#boton_info_comarques").css("background-color","lightgreen");
        modo_info_comarques=true;
        $(".leaflet-container").css( 'cursor', 'crosshair' );
    }
}
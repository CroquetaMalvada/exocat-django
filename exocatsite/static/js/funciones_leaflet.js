$(document).ready(function(){
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) { //Actualizamos el mapa cuando el usuario clica en la pestana mapa del dialog
        if($(e.target).attr("value"))
            if($(e.target).attr("id")=="mapa_de_especie"){
                map_info_especie.invalidateSize(false);
                obtener_pos_especie();
            }
    });
});

function obtener_pos_especie(){
id=$("#mapa_de_especie").attr("value");
//    if(wmsLayer_presencia_10000!=false)

    // OJO QUE LOS ID CAMBIAN !
mapainfo_wmsLayer_presencia_10000.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});
mapainfo_wmsLayer_presencia_1000.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});
mapainfo_wmsLayer_citacions.setParams({cql_filter:"idspinvasora='"+id+"'"});
mapainfo_wmsLayer_presencia_ma.setParams({cql_filter:"idtaxon='"+id+"'"});


//    if(wmsLayer_presencia_10000!=false)
//        mymap.removeLayer(wmsLayer_presencia_10000);
//
//    wmsLayer_presencia_10000 = L.tileLayer.wms('http://exocat2.creaf.cat/geoserver/wms?', {
//        layers: 'SIPAN:PRESENCIA_SP_10000',
//        transparent: 'true',
//        format: 'image/png',
//        cql_filter: "IDSPINVASORA='"+id+"'"
//    });
//
//    mymap.addLayer(wmsLayer_presencia_10000);
    //control.selectLayer(wmsLayer_presencia_10000);
}

function obtener_especies_geom(){ // OBTENER ESPECIES DE RECTANGULO O FIGURA(aqui se usa la datatable)
    cargando_datos_mapa(0);
    var filtro= pasar_wkt();
//    alert("INTERSECTS(geom_4326,"+filtro+")");
    // mostramos las layers(cuadriculas,citacions,rius,etc) que hay en la zona marcada
    wmsLayer_presencia_10000.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_presencia_1000.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_citacions.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_presencia_ma.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});


    $.ajax({
        url:"/especies_seleccion/",
        data:{"pol":filtro},
//        type:'json',
        success: function (data, status, xhr) {
            //console.log(data);
            rellenar_table_especies_seleccion(data);
            cargando_datos_mapa(1);
        },
        error: function (xhr, status, error) {
            alert("error");
            cargando_datos_mapa(2);
        }
    });
}
function pasar_wkt(){ // pasa las selecciones/geometrias a wkt
    var geojson = editableLayers.toGeoJSON();
    var wkt = new Wkt.Wkt();
    wkt.read( JSON.stringify(geojson.features[0].geometry) );
    //console.log(wkt.write());
    return wkt.write();
}

function obtener_especies_pos(latlng){// OBTENER ESPECIES DEL CLICK(aqui se usa la datatable)

///////////// PARTE 1,INDICAR SOBRE QUE CAPAS(CAPA EN ESTE CASO) HAY QUE OBTENER LA POSICION DEL CLICK
    cargando_datos_mapa(0);
    //mymap.removeLayer(wmsLayer_presencia_10000);

    var layers_in_control = [];
    layers_in_control.push(wmsLayer_presencia_10000);
//            layers_in_control.push(wmsLayer_presencia_1000);
    if(layers_in_control.length > 0){
        var param_layers = [];
        for(var i=0; i < layers_in_control.length; i++){
            param_layers.push( layers_in_control[i].wmsParams.layers );
        }
        var querylayers = param_layers.join(',');
        //getFeatureInfo(evt,querylayers);

        //////////// PARTE 2,CREAR UNA URL PARA PEDIR AL SERVIDOR LAS ESPECIES DE DICHA POSICION

        var point="";
        if(latlng) // si le pasamos el punto de google maps donde clicamos...
            point = mymap.latLngToContainerPoint(latlng, mymap.getZoom());

        var size = mymap.getSize();
        var url="";

//        if(tipo==1){ // si es de un punto
        var params = {
            request: 'GetFeatureInfo',
            service: 'WMS',
            srs: 'EPSG:4326',
            styles: '',
            transparent: true,
            version: '1.1.1',
            format: 'image/jpeg',
            bbox: mymap.getBounds().toBBoxString(),
            height: size.y,
            width: size.x,
            layers: querylayers,
            query_layers: querylayers,
            info_format: 'application/json',
            feature_count: 100000000
        };
        // segun la version se usa x o i para especificar el pixel de busqueda
        params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
        params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

        wms_url = "http://exocatdb.creaf.cat/geoserver/wms";
        url = wms_url + L.Util.getParamString(params, wms_url, true);
//        }else if(tipo==2){// si es una comarca
////            var bbox=a1,b1,a2,b2;
//            //url = "http://exocat2.creaf.cat/geoserver/wfs?outputFormat=application/json&service=wfs&version=2.0.0&request=GetFeature&typeNames=SIPAN:PRESENCIA_SP_10000_p&srsName=EPSG:23031&41.812744811244976,1.1476136371493342,42.21678824705352,1.7848206683993342";
//        }

        ////////// PARTE 3,USAMOS LA URL PARA HACER UNA PETICION AJAX
        $.ajax({
            url: "/especies_de_cuadro/",
            data:{'url':url},
            //type:'json',
            success: function (data, status, xhr) {
//                console.log(data);
//                var err = typeof data === 'string' ? null : data;
//                if(err){
//                    alert("error");
//                }else{
                ////////// PARTE 4,UNA VEZ OBTENIDOS LOS DATOS,OBTENEMOS LO QUE NOS INTERESE Y LO USAMOS PARA MOSTRARLO EN PANTALLA
//
//                $.ajax({
//                    url:"/citacions_especie/",
//                    data:{'id':this.properties.IDSPINVASORA},
//                    success:function(){}
//                 });
//                console.log(data);
                rellenar_table_especies_click(data);
//                }

                //showGetFeatureInfo(err, evt.latlng, data);
                cargando_datos_mapa(1);
            },
            error: function (xhr, status, error) {
                alert("error");
                cargando_datos_mapa(2);
                //showGetFeatureInfo(error);
            }
        });
    }
}


function obtener_especies_comarca(latlng){// OBTENER ESPECIES DE COMARCA( se usa datatable)

///////////// PARTE 1,INDICAR SOBRE QUE CAPAS(CAPA EN ESTE CASO) HAY QUE OBTENER LA POSICION DEL CLICK
    cargando_datos_mapa(0);

    var layers_in_control = [];
    layers_in_control.push(wmsLayer_comarques);
    if(layers_in_control.length > 0){
        var param_layers = [];
        for(var i=0; i < layers_in_control.length; i++){
            param_layers.push( layers_in_control[i].wmsParams.layers );
        }
        var querylayers = param_layers.join(',');
        //////////// PARTE 2,CREAR UNA URL PARA PEDIR AL SERVIDOR LAS ESPECIES DE DICHA POSICION
        var point="";
        if(latlng) // si le pasamos el punto de google maps donde clicamos...
            point = mymap.latLngToContainerPoint(latlng, mymap.getZoom());

        var size = mymap.getSize();
        var url="";

        var params = {
            request: 'GetFeatureInfo',
            service: 'WMS',
            srs: 'EPSG:4326',
            styles: '',
            transparent: true,
            version: '1.1.1',
            format: 'image/jpeg',
            bbox: mymap.getBounds().toBBoxString(),
            height: size.y,
            width: size.x,
            layers: querylayers,
            query_layers: querylayers,
            info_format: 'application/json',
            feature_count: 100000000
        };
        // segun la version se usa x o i para especificar el pixel de busqueda
        params[params.version === '1.3.0' ? 'i' : 'x'] = point.x;
        params[params.version === '1.3.0' ? 'j' : 'y'] = point.y;

        wms_url = "http://exocatdb.creaf.cat/geoserver/wms";
        url = wms_url + L.Util.getParamString(params, wms_url, true);
        ////////// PARTE 3,USAMOS LA URL PARA HACER UNA PETICION AJAX(esta nos dara la geom de la comarca
        $.ajax({
            url: "/especies_de_comarca/",
            data:{'url':url},
            success: function (data, status, xhr) {

//                var wkt = new Wkt.Wkt();
//                wkt.read( JSON.stringify(data[0]["geom"]) );
//                filtro = wkt.write();

                var filtro = data[0]["filtro"];
                ///// PARTE 4,CON LA GEOM DE LA COMARCA HACEMOS UN INTERSECTS Y UTILIZAMOS LA MISMA FUNCION QUE LA DE CALCULAR ESPECIES POR SELECCION
                // mostramos las layers(cuadriculas,citacions,rius,etc) que hay en la zona marcada
                wmsLayer_presencia_10000.setParams({cql_filter:"INTERSECTS(geom,"+filtro+")"});
//                wmsLayer_presencia_1000.setParams({cql_filter:"INTERSECTS(geom,"+filtro+")"});
//                wmsLayer_citacions.setParams({cql_filter:"INTERSECTS(geom,"+filtro+")"});
//                wmsLayer_presencia_ma.setParams({cql_filter:"INTERSECTS(geom,"+filtro+")"});
                mymap.addLayer(wmsLayer_presencia_10000);
//                $.ajax({
//                    url:"/especies_seleccion/",
//                    data:{"pol":filtro},
//                    success: function (data, status, xhr) {
//                        //console.log(data);
//                        rellenar_table_especies_seleccion(data);
//                        cargando_datos_mapa(1);
//                    },
//                    error: function (xhr, status, error) {
//                        alert("error");
//                        cargando_datos_mapa(2);
//                    }
//                });
                rellenar_table_especies_seleccion(data[0]["geom"]);
                cargando_datos_mapa(1);
            },
            error: function (xhr, status, error) {
                alert("error");
                cargando_datos_mapa(2);
            }
        });
    }
}


function limpiar_mapa(){
    editableLayers.clearLayers(wmsLayer_presencia_10000);
}
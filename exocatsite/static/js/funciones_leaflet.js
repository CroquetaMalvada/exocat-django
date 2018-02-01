$(document).ready(function(){
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) { //Actualizamos el mapa cuando el usuario clica en la pestana mapa del dialog
        if($(e.target).attr("value"))
            if($(e.target).attr("id")=="mapa_de_especie"){
                mymap.invalidateSize(false);
                obtener_pos_especie();
            }
    });
});

function obtener_pos_especie(){
id=$("#mapa_de_especie").attr("value");
//    if(wmsLayer_presencia_10000!=false)

wmsLayer_presencia_10000.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});
wmsLayer_presencia_1000.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});
wmsLayer_citacions.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});
wmsLayer_presencia_ma.setParams({cql_filter:"IDSPINVASORA='"+id+"'"});


//    if(wmsLayer_presencia_10000!=false)
//        mymap.removeLayer(wmsLayer_presencia_10000);
//
//    wmsLayer_presencia_10000 = L.tileLayer.wms('http://montesdata.creaf.cat/geoserver/wms?', {
//        layers: 'SIPAN:PRESENCIA_SP_10000',
//        transparent: 'true',
//        format: 'image/png',
//        cql_filter: "IDSPINVASORA='"+id+"'"
//    });
//
//    mymap.addLayer(wmsLayer_presencia_10000);
    //control.selectLayer(wmsLayer_presencia_10000);
}

function obtener_especies_geom(){
    var filtro= pasar_wkt();
//    alert("INTERSECTS(geom_4326,"+filtro+")");
    // mostramos las layers(cuadriculas,citacions,rius,etc) que hay en la zona marcada
    wmsLayer_presencia_10000.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_presencia_1000.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_citacions.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});
    wmsLayer_presencia_ma.setParams({cql_filter:"INTERSECTS(geom_4326,"+filtro+")"});

    //ahora las especies que hay en los cuadros de 10 km
    taula_especies_map.clear();
    taula_especies_map.row.add(["Carregant dades...",""]);
    $.ajax({
        url:"/especies_seleccion/",
        data:{"pol":filtro},
//        type:'json',
        success: function (data, status, xhr) {
            console.log(data);
            taula_especies_map.clear();
            $(data).each(function(){
                console.log(this);
                taula_especies_map.row.add([
                    this.nom,
                    '<a class="btn btn-info mostrar_info_especie" value="'+this.id+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>'
                ]);
            });
            taula_especies_map.draw();
        },
        error: function (xhr, status, error) {
            alert("error");
        }
    });
}
function pasar_wkt(){ // pasa las selecciones/geometrias a wkt
    var geojson = editableLayers.toGeoJSON();
    var wkt = new Wkt.Wkt();
    wkt.read( JSON.stringify(geojson.features[0].geometry) );
    console.log(wkt.write());
    return wkt.write();
}

function obtener_especies_pos(latlng,tipo){

///////////// PARTE 1,INDICAR SOBRE QUE CAPAS(CAPA EN ESTE CASO) HAY QUE OBTENER LA POSICION DEL CLICK

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

        var point=""
        if(latlng) // si le pasamos el punto de google maps donde clicamos...
            point = mymap.latLngToContainerPoint(latlng, mymap.getZoom());

        var size = mymap.getSize();
        var url="";

        if(tipo==1){ // si es de un punto
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

            wms_url = "http://montesdata.creaf.cat/geoserver/wms";
            url = wms_url + L.Util.getParamString(params, wms_url, true);
        }else if(tipo==2){// si son las que hay en los puntos dentro de una caja
//            var bbox=a1,b1,a2,b2;
            url = "http://montesdata.creaf.cat/geoserver/wfs?outputFormat=application/json&service=wfs&version=2.0.0&request=GetFeature&typeNames=SIPAN:PRESENCIA_SP_10000_p&srsName=EPSG:23031&41.812744811244976,1.1476136371493342,42.21678824705352,1.7848206683993342";
        }

        ////////// PARTE 3,USAMOS LA URL PARA HACER UNA PETICION AJAX

        $.ajax({
            url: url,
            //type:'json',
            success: function (data, status, xhr) {
                console.log(data);
//                var err = typeof data === 'string' ? null : data;
//                if(err){
//                    alert("error");
//                }else{
                ////////// PARTE 4,UNA VEZ OBTENIDOS LOS DATOS,OBTENEMOS LO QUE NOS INTERESE Y LO USAMOS PARA MOSTRARLO EN PANTALLA
                taula_especies_map.clear();
                $(data.features).each(function(){
//                    console.log(this);
                    taula_especies_map.row.add([
                        this.properties.nom,
                        '<a class="btn btn-info mostrar_info_especie" value="'+this.properties.IDSPINVASORA+'" title="Info" href="#"><i class="fa fa-eye fa-lg"></i></a>'
                    ]).draw();
                    //alert(this.properties.IDSPINVASORA);
                });
//                }

                //showGetFeatureInfo(err, evt.latlng, data);
            },
            error: function (xhr, status, error) {
                alert("error");
                //showGetFeatureInfo(error);
            }
        });
    }
}

function limpiar_mapa(){
    editableLayers.clearLayers(wmsLayer_presencia_10000);
}
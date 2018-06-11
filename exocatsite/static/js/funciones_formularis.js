var espai_natural_protegit="no";
var espai_natural_nom="";
var nuevo=1;
var id_form;
var cargar_especie="";

$(document).ready(function(){

    $("#id_data").datepicker({ dateFormat: 'dd-mm-yy' , TimePicker: false});

    $("#formulari_localitats_especie").find("input").each(function(){
        if($(this).attr('type')!='radio' && $(this).attr('type')!='checkbox'){
            $(this).attr('class','form-control');
        }
    });

    //mostrar/ocultar/deshabilitar los diferentes inputs en funcion e la seleccion del usuario
    $("#id_idspinvasora").change(function(){
        check_select_especie();
    });

    $("input[name=tipus_coordenades]").change(function(){
        check_coordenades();
    });

    $("input[name=espai_natural_protegit]").change(function(){
        check_espai_natural();
    });

    $("input[name=tipus_espai_natural_protegit]").change(function(){
        check_espai_natural_altres($(this));
    });

    //
    if(nuevo==0){
        $("#id_idspinvasora").val(cargar_especie);
        $("#id_espai_nom").val(espai_natural_nom);
        check_select_especie();
        check_coordenades();
    }else{
        cargar_default();
    }

    //
    $("#autoritzacio").change(function(){
        if($(this).is(":checked")){
            $("#boton_enviar").attr("disabled",false);
        }else{
            $("#boton_enviar").attr("disabled",true);
        }
    })
    /// OJO CREAR FUNCION QUE CARGA UN FORMULARIO
    $(".errorlist").each(function(){
        $(this).addClass("text-danger");
        $(this).prev("input").addClass("is-invalid");
    });

    if(espai_natural_protegit=="si"){
        $("#id_espai_natural_protegit_1").click();
        if(espai_natural_nom == "ENPE" || espai_natural_nom == "PEIN" || espai_natural_nom == "XN2000" ){
                $("#contenedor_si_espai_natural :input[value='"+espai_natural_nom+"']").click();
        }else{
            $("#tipus_espai_natural_altres").click();
        }
    }else{
        $("#id_espai_natural_protegit_0").click();
    }

    $("#id_espai_nom").val(espai_natural_nom);


    ///////////// CARGAR IMAGENES
    // CARGAR IMAGEN PRINCIPAL
    $.ajax({
        type: "GET",
        data: {"id_imatge_principal":$("#id_imatge_principal").attr("value")},
        url: "/upload_imatge_citacions_especie/",
        success: function(data) {
            $("#foto_principal_gallery").append(
              "<img width='200' src='" + data.url + "'></img>  <br>"+data.name
            );
        },
        complete:function(){
            // CARGAR IMAGENES SECUNDARIAS
            if($("#ids_imatges").val()!=""){
                $.ajax({
                    type: "GET",
                    data: {"ids_imatges":$("#ids_imatges").attr("value")},
                    url: "/upload_imatge_citacions_especie/",
                    success: function(data) {
                        //console.log(data);
                        $.each(data,function(){
                            //$("#ids_imatges").val($("#ids_imatges").val()+this.id+",");
                            $("#gallery tbody").prepend(
                              "<tr><td><img width='100' src='" + this.url + "'></img>  "+this.name+"</td></tr>"
                            );
                        });
                    }
                });
            }else{
                mostrar_ocultar_dades_opcionals();
            }
        }
    });


    //crear tooltips
    $(".boton_tooltip").tooltip();
//    Cookies.set('proyectos',proyectos, { expires: 1 });
});

function cargar_default(){
    // OJO seguir reseteando o no el formulario tras cada refresh?
//    $("#formulari_localitats_especie")[0].reset();
    //
    check_select_especie();
    check_coordenades();
    check_espai_natural();
    check_espai_natural_altres();
//    $("#id_presencia_0").click();
//    $("#id_qual_terreny_0").click();
}

function check_select_especie(){
    if($("#id_idspinvasora").val()=="00000"){
        $("#id_especie").attr("disabled",false);
    }else{
        $("#id_especie").val("");
        $("#id_especie").attr("disabled",true);
    }
}

function check_coordenades(){
    if($("#coordenada_1").is(":checked")){
        //enable
        $("#id_utmx").attr("disabled",false);
        $("#id_utmy").attr("disabled",false);
        $("#id_utmz").attr("disabled",false);
        //disable
        $("#id_utm_10").val("");
        $("#id_utm_10").attr("disabled",true);

        $("#id_utm_1").val("");
        $("#id_utm_1").attr("disabled",true);

    }if($("#coordenada_2").is(":checked")){
        //enable
        $("#id_utm_10").attr("disabled",false);
        //disable
        $("#id_utmx").val("");
        $("#id_utmx").attr("disabled",true);
        $("#id_utmy").val("");
        $("#id_utmy").attr("disabled",true);
        $("#id_utmz").val("");
        $("#id_utmz").attr("disabled",true);

        $("#id_utm_1").val("");
        $("#id_utm_1").attr("disabled",true);
    }if($("#coordenada_3").is(":checked")){
        //enable
        $("#id_utm_1").attr("disabled",false);
        //disable
        $("#id_utmx").val("");
        $("#id_utmx").attr("disabled",true);
        $("#id_utmy").val("");
        $("#id_utmy").attr("disabled",true);
        $("#id_utmz").val("");
        $("#id_utmz").attr("disabled",true);

        $("#id_utm_10").val("");
        $("#id_utm_10").attr("disabled",true);
    }
}

function check_espai_natural(){
    if($("#id_espai_natural_protegit_0").is(":checked")){ // el 0 es el "no"
        $("#contenedor_si_espai_natural").hide();
    }else{
        $("#contenedor_si_espai_natural").show();
    }
}

function check_espai_natural_altres(check){
    if($("#tipus_espai_natural_altres").is(":checked")){
        $("#id_espai_nom").val("");
        $("#contenedor_si_espai_natural_altres").show();
    }else{
        $("#id_espai_nom").val($(check).val());
        $("#contenedor_si_espai_natural_altres").hide();
    }
}
function mostrar_ocultar_dades_opcionals(){
    if($("#div_dades_opcionals").is(":visible")){
        $("#div_dades_opcionals").hide();
    }else{
        $("#div_dades_opcionals").show();
    }


}
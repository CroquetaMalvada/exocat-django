# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
from django.db.models import Q
from exocatsite.models import *#Grup,Grupespecie,Viaentrada,Viaentradaespecie,Estatus,Especieinvasora,Taxon,Nomvulgar,Nomvulgartaxon,Habitat,Habitatespecie,Regionativa,Zonageografica,Imatges,Imatge
from django.contrib.gis.geos import GEOSGeometry
import json, urllib

# Create your views here.
def view_base_dades(request):
    context = {'especies_invasores': "", 'titulo': "ESPECIES INVASORES"}
    return render(request, 'exocat/base_dades.html', context)

# mapa
def view_mapa(request):
    # context = {'especies_invasores': "", 'titulo': "ESPECIES INVASORES"}
    return render(request, 'exocat/mapa.html')

# JSON DE FILTRES
def json_select_groups(request):
    grups= Grup.objects.all().order_by("nom")
    resultado=[]
    for grup in grups:
        resultado.append({'id':str(grup.id),'nom': grup.nom})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

def json_select_viaentrada(request):
    vies= Viaentrada.objects.all().order_by("viaentrada")
    resultado=[]
    for via in vies:
        resultado.append({'id':str(via.id),'nom': via.viaentrada})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

def json_select_estatus(request):
    estatus= Estatus.objects.all().order_by("nom")
    resultado=[]
    for estat in estatus:
        resultado.append({'id':str(estat.id),'nom': estat.nom})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

def json_select_regionativa(request):
    regions= Zonageografica.objects.all().order_by("nom")
    resultado=[]
    for regio in regions:
        resultado.append({'id':str(regio.id),'nom': regio.nom})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

#DATATABLES
def json_taula_especies(request):
    especies= Especieinvasora.objects.all().order_by("idtaxon__genere").values("id","idtaxon__genere","idtaxon__especie","idtaxon__subespecie")
    resultado=[]
    for especie in especies:
        # nombre de la especie(se juntan el genere con especie y subespecie)
        id=str(especie["id"])
        genere=str(especie["idtaxon__genere"])
        especiestr=especie["idtaxon__especie"]
        subespeciestr = especie["idtaxon__subespecie"]
        if especiestr is not None:
            genere=genere+" "+str(especiestr)
        if subespeciestr is not None:
            genere = genere + " [subespecie: "+str(subespeciestr)+" ]"

        #grupo
        grup=Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom

        # #variedad(se junta con subvariedad)
        # varietat=""
        # if especie.idtaxon.varietat is not None:
        #     varietat = varietat+str(especie.idtaxon.varietat)
        # if especie.idtaxon.subvarietat is not None:
        #     varietat = varietat+" - "+str(especie.idtaxon.subvarietat)
        #
        # # #nombres vulgares *descartado por ahora
        # # nomsvulgars=""
        # # # for nomv in Nomvulgartaxon.objects.filter(idtaxon=especie.idtaxon):
        # # #     nomsvulgars=nomsvulgars+nomv.idnomvulgar.nomvulgar+","
        # #
        # # #habitat !Ojo de momento esta tabla esta vacia en la bdd
        # # # habitat=Habitatespecie.objects.get(idspinvasora=especie.id).idspinvasora.habitat
        #
        # #Estatus Catalunya
        # estatuscat= especie.idestatuscatalunya.nom
        #
        # #Region nativa
        # try:# hacemos try porque hay algunos en los que es nulo(?) y peta
        #     regionativa=Regionativa.objects.get(idespecieinvasora=especie.id).idzonageografica.nom
        # except:
        #     regionativa=""#"Desconeguda"
        #
        # # Via de entrada
        # viaentrada=''
        # for via in Viaentradaespecie.objects.filter(idespecieinvasora=especie.id):
        #     if viaentrada=='':
        #         viaentrada= viaentrada+str(via.idviaentrada.viaentrada)
        #     else:
        #         viaentrada = viaentrada+', '+ str(via.idviaentrada.viaentrada)
        #
        # # Estatus Historic
        # try:
        #     estatushistoric = especie.idestatushistoric.nom
        # except:
        #     estatushistoric = ""
        #
        # # Presente en el 'Catálogo espanol de especies exoticas invasoras'
        # present=especie.present_catalogo

        # # viaentrada=Viaentradaespecie.objects.get(idespecieinvasora=especie.id).idviaentrada.viaentrada
        resultado.append({'id':id,'especie': genere,'grup':grup}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':str(especie.id),'especie': genere,'grup':grup, 'varietat':varietat, 'regionativa':regionativa, 'estatuscat':estatuscat,'viaentrada':viaentrada, 'estatushistoric':estatushistoric, 'present':present}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':"",'especie':"",'grup':"", 'varietat':"", 'regionativa':"", 'estatuscat':"",'viaentrada':"", 'estatushistoric':"", 'present':""}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat

    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

#ESPECIES FILTRADAS
def json_taula_especies_filtres(request):
    campos=request.POST

    # CREAMOS LOS FILTROS:
    estatus = Estatus.objects.all().values("id") #lo metemos en una variable ya que esta lista la usaremos en mas de una ocasion en los filtros

    def filtro_nombre():
        if campos["especie"] is not "":
            return (Q(idtaxon__genere__icontains=campos["especie"]) | Q(idtaxon__especie__icontains=campos["especie"]) | Q (idtaxon__subespecie__icontains=campos["especie"]))
        else:
            return Q(id__isnull=False)

    def filtro_grups():
        if campos["grups"] is not "":
            return Q(id__in=Grupespecie.objects.filter(idgrup=campos["grups"]).values("idespecieinvasora"))
        else:
            return Q(id__isnull=False)

    def filtro_estatus_cat():
        if campos["estatuscatalunya"] is not "":
            return Q(idestatuscatalunya=campos["estatuscatalunya"])
        else:
            return Q(id__isnull=False)

    def filtro_varietat():
        if campos["varietat"] is not "":
            return (Q(idtaxon__varietat__icontains=campos["varietat"]) | Q(idtaxon__subvarietat__icontains=campos["varietat"]))
        else:
            return Q(id__isnull=False)

    def filtro_regiones():
        if campos["regionativa"] is not "":
            return Q(id__in=Regionativa.objects.filter(idzonageografica=campos["regionativa"]).values("idespecieinvasora"))
        else:
            return Q(id__isnull=False)

    def filtro_vias_entrada():
        if campos["viaentrada"] is not "":
            return Q(id__in=Viaentradaespecie.objects.filter(idviaentrada=campos["viaentrada"]).values("idespecieinvasora"))
        else:
            return Q(id__isnull=False)

    def filtro_estatus_historico():
        if campos["estatushistoric"] is not "":
            return Q(idestatushistoric=campos["estatushistoric"])
        else:
            return Q(id__isnull=False)

    def filtro_catalogo():
        if campos["present_catalog"] is not "":
            return Q(present_catalogo=campos["present_catalog"])
        else:
            return Q(id__isnull=False)


    # APLICAMOS LOS FILTROS:

    especies= Especieinvasora.objects.filter(
        # para el nombre(campo especie) !Ojo __icontains no es sensible a mayusculas a diferencia de __contains!
        filtro_nombre(),

        #para los grups
        filtro_grups(),

        #para estatus catalunya
        filtro_estatus_cat(),

        #para varietat
        filtro_varietat(),

        # para las regiones nativas
        filtro_regiones(),

        # para las vias de entrada
        filtro_vias_entrada(),

        # para el estatus historico
        filtro_estatus_historico(),

        # para el present al catalogo
        filtro_catalogo()

    ).order_by("idtaxon__genere").values("id","idtaxon__genere","idtaxon__especie","idtaxon__subespecie")

    # FINALMENTE DEVOLVEMOS CADA ESPECIE QUE HAYA PASADO LOS FILTROS:
    resultado=[]
    for especie in especies:
        # nombre de la especie(se juntan el genere con especie y subespecie)
        id=str(especie["id"])
        genere=str(especie["idtaxon__genere"])
        especiestr=especie["idtaxon__especie"]
        subespeciestr = especie["idtaxon__subespecie"]
        if especiestr is not None:
            genere=genere+" "+str(especiestr)
        if subespeciestr is not None:
            genere = genere + " [subespecie: "+str(subespeciestr)+" ]"

        #grupo
        grup=Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom

        # # viaentrada=Viaentradaespecie.objects.get(idespecieinvasora=especie.id).idviaentrada.viaentrada
        resultado.append({'id':id,'especie': genere,'grup':grup}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':str(especie.id),'especie': genere,'grup':grup, 'varietat':varietat, 'regionativa':regionativa, 'estatuscat':estatuscat,'viaentrada':viaentrada, 'estatushistoric':estatushistoric, 'present':present}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':"",'especie':"",'grup':"", 'varietat':"", 'regionativa':"", 'estatuscat':"",'viaentrada':"", 'estatushistoric':"", 'present':""}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat

    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

# INFO DE UNA ESPECIE
def json_info_especie(request):
    info=request.POST
    id = info["id"]
    especieinvasora = Especieinvasora.objects.values_list('idtaxon','idtaxon__genere','idtaxon__especie','idtaxon__subespecie','idtaxon__varietat','idtaxon__subvarietat').get(id=info["id"])
    id_taxon=especieinvasora[0]
    genere= especieinvasora[1]
    especie=especieinvasora[2]
    subespecie=especieinvasora[3]
    varietat=especieinvasora[4]
    subvarietat=especieinvasora[5]
    nomsvulgars=""

    # OJO que los datos de citacions a excepcion de ncitacions no se utilizaran por ahora
    citacions= Citacions.objects.filter(idspinvasora=id).values("citacio","localitat","municipi","comarca","provincia","data","autor_s","font")
    ncitacions = Citacions.objects.filter(idspinvasora=id).count()

    # calcular el numero de masas de agua y el numero de utms de una especie
    id_exoaqua= ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
    massesaigua = []
    nmassesaigua=0

    nutm1000=0
    nutm10000=0
    utms= PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
    for utm in utms:
        if utm["idquadricula__resolution"]==10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
            nutm1000=nutm1000+1
        if utm["idquadricula__resolution"]==1000:
            nutm10000 = nutm10000 + 1



    if id_exoaqua: # si existe una relacion de exoaqua-exocat de dicha especie
        id_exoaqua=id_exoaqua[0]["id_exoaqua"] # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
        id_massesaigua= MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).values("id_localitzacio")

        for id_massa in id_massesaigua:
            try:
                massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
                nom=massa.nom
            except:
                nom="# Sense Dades #"
            try:
                massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
                tipus=massa.id_categor
            except:
                tipus="# Sense Dades #"
            try:
                massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
                conca=ConquesPrincipals.objects.filter(id=massa.idconca).values("nom_conca").first()
            except:
                conca="# Sense Dades #"

            massesaigua.append({"nom":nom,"tipus":tipus,"conca":conca})
        nmassesaigua= MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()#Ojo mirar bien esto!!!

    #

    for nomv in Nomvulgartaxon.objects.filter(idtaxon=id_taxon):
        if nomv=="":
            nomsvulgars=nomv.idnomvulgar.nomvulgar
        else:
            nomsvulgars=nomsvulgars+nomv.idnomvulgar.nomvulgar+","

    grup = Grupespecie.objects.get(idespecieinvasora=info["id"]).idgrup.nom
    regionativa=""
    try:# hacemos try porque hay algunos en los que es nulo(?) y peta
        regionativa=Regionativa.objects.get(idespecieinvasora=especie.info["id"]).idzonageografica.nom
    except:
        regionativa=""#"Desconeguda"

    try:
        estatushistoric=Especieinvasora.objects.get(id=info["id"]).idestatushistoric.nom
    except:
        estatushistoric=""
    try:
        estatuscatalunya=Especieinvasora.objects.get(id=info["id"]).idestatuscatalunya.nom
    except:
        estatuscatalunya =""


    viesentrada=""
    for via in Viaentradaespecie.objects.filter(idespecieinvasora=info["id"]):
        if viesentrada=='':
            viesentrada= viesentrada+str(via.idviaentrada.viaentrada)
        else:
            viesentrada = viesentrada+', '+ str(via.idviaentrada.viaentrada)

    presentcatalog=Especieinvasora.objects.get(id=info["id"]).present_catalogo
    if presentcatalog=="S":
        presentcatalog="Si"
    else:
        presentcatalog="No"

    observacions=Especieinvasora.objects.get(id=info["id"]).observacions

    titolimatge=Imatge.objects.filter(idespecieinvasora=info["id"]).values("idimatge__titol")
    if not titolimatge:
        titolimatge="IMATGE NO DISPONIBLE"
    else:
        titolimatge=titolimatge[0]["idimatge__titol"] # obtenemos el titulo de la primera imagen(ya que en la baswe de datos no hay nada en idimatgeprincipal
    imatges_especie=[]
    for img in Imatge.objects.filter(idespecieinvasora=info["id"]).values("idimatge","idimatge__titol","idimatge__idextensio"):
        imatges_especie.append({"id":img["idimatge"],"titol":img["idimatge__titol"],"extensio":img["idimatge__idextensio"]})


    # try:
    #     titolimatge=Especieinvasora.objects.get(id=info["id"]).idimatgeprincipal
    # except:
    #     titolimatge=""

    # #variedad(se junta con subvariedad)
    # varietat=""
    # if especie.idtaxon.varietat is not None:
    #     varietat = varietat+str(especie.idtaxon.varietat)
    # if especie.idtaxon.subvarietat is not None:
    #     varietat = varietat+" - "+str(especie.idtaxon.subvarietat)
    #
    # # #nombres vulgares *descartado por ahora
    # # nomsvulgars=""
    # # # for nomv in Nomvulgartaxon.objects.filter(idtaxon=especie.idtaxon):
    # # #     nomsvulgars=nomsvulgars+nomv.idnomvulgar.nomvulgar+","
    # #
    # # #habitat !Ojo de momento esta tabla esta vacia en la bdd
    # # # habitat=Habitatespecie.objects.get(idspinvasora=especie.id).idspinvasora.habitat
    #
    # #Estatus Catalunya
    # estatuscat= especie.idestatuscatalunya.nom
    #
    # #Region nativa
    # try:# hacemos try porque hay algunos en los que es nulo(?) y peta
    #     regionativa=Regionativa.objects.get(idespecieinvasora=especie.id).idzonageografica.nom
    # except:
    #     regionativa=""#"Desconeguda"
    #
    # # Via de entrada
    # viaentrada=''
    # for via in Viaentradaespecie.objects.filter(idespecieinvasora=especie.id):
    #     if viaentrada=='':
    #         viaentrada= viaentrada+str(via.idviaentrada.viaentrada)
    #     else:
    #         viaentrada = viaentrada+', '+ str(via.idviaentrada.viaentrada)
    #
    # # Estatus Historic
    # try:
    #     estatushistoric = especie.idestatushistoric.nom
    # except:
    #     estatushistoric = ""
    #
    # # Presente en el 'Catálogo espanol de especies exoticas invasoras'
    # present=especie.present_catalogo
    resultado=json.dumps({'id':info["id"],'genere':genere,'especie':especie,'subespecie':subespecie,'varietat':varietat,'subvarietat':subvarietat,'nomsvulgars':nomsvulgars,'grup':grup,'regionativa':regionativa,'estatushistoric':estatushistoric,'estatuscatalunya':estatuscatalunya,'viesentrada':viesentrada,'presentcatalog':presentcatalog,'observacions':observacions,'imatges':imatges_especie,'titolimatge':titolimatge,'nutm1000':nutm1000,'nutm10000':nutm10000,'ncitacions':ncitacions,'nmassesaigua':nmassesaigua})
    return HttpResponse(resultado, content_type='application/json;')

#ESPECIES DE X COORDENADAS
# def json_especies_de_coordenadas(request):
#     lat=request.GET["lat"]
#     long=request.GET["long"]
#
#     # Create the cursor
#     cursor = connection.cursor()
#
#
#     # Execute the SQL
#     cursor.execute('SELECT * FROM exocat.sipan_mexocat.presencia_sp')
#     result = cursor.fetchall()
#
#     return result


#ESPECIES EN UN CUADRO DE 10KM(EN REALIDAD SE OBTIENE UN RECUADRO DE UN CLICK)
def json_especies_de_cuadro(request):
    url=request.GET["url"]
    response=urllib.urlopen(url)
    data = json.loads(response.read())
    resultado=[]
    for especie in data["features"]:
        id=especie["properties"]["IDSPINVASORA"]
        id_taxon=Especieinvasora.objects.values_list('idtaxon').get(id=id)[0]
        # calcular el numero de masas de agua y el numero de utms de una especie
        id_exoaqua = ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
        massesaigua = []
        nmassesaigua = 0

        nutm1000 = 0
        nutm10000 = 0
        utms = PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
        for utm in utms:
            if utm["idquadricula__resolution"] == 10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
                nutm1000 = nutm1000 + 1
            if utm["idquadricula__resolution"] == 1000:
                nutm10000 = nutm10000 + 1

        if id_exoaqua:  # si existe una relacion de exoaqua-exocat de dicha especie
            id_exoaqua = id_exoaqua[0]["id_exoaqua"]  # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
            nmassesaigua = MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()  # Ojo mirar bien esto!!!

        #
        ncitacions=Citacions.objects.filter(idspinvasora=id).count()

        dades=PresenciaSp.objects.filter(idspinvasora=id).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")
        nom=str(dades[0]["idspinvasora__idtaxon__genere"])+" "+str(dades[0]["idspinvasora__idtaxon__especie"])
        resultado.append({"nom":nom,"id":dades[0]["idspinvasora"],"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')


#ESPCEIES EN LOS CUADROS DE 10 KM QUE HAY EN UNA SELECCION
def json_especies_de_seleccion(request):
    pol=request.GET["pol"]
    # pasamos el poligono a 4326
    poligono= GEOSGeometry(pol, srid=4326)
    # quadriculas de 10km que intersectan con el poligono
    quad = Quadricula.objects.filter(geom_4326__intersects=poligono) # quitamos el .filter(resolution=10000)
    especies = PresenciaSp.objects.filter(idquadricula__in=quad).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")
    resultado=[]
    for especie in especies:
        id=especie["idspinvasora"]
        id_taxon = Especieinvasora.objects.values_list('idtaxon').get(id=id)[0]
        # calcular el numero de masas de agua y el numero de utms de una especie
        id_exoaqua = ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
        massesaigua = []
        nmassesaigua = 0

        nutm1000 = 0
        nutm10000 = 0
        utms = PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
        for utm in utms:
            if utm["idquadricula__resolution"] == 10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
                nutm1000 = nutm1000 + 1
            if utm["idquadricula__resolution"] == 1000:
                nutm10000 = nutm10000 + 1

        if id_exoaqua:  # si existe una relacion de exoaqua-exocat de dicha especie
            id_exoaqua = id_exoaqua[0]["id_exoaqua"]  # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
            nmassesaigua = MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()  # Ojo mirar bien esto!!!

        #

        ncitacions = Citacions.objects.filter(idspinvasora=id).count()

        resultado.append({"nom":especie["idspinvasora__idtaxon__genere"]+" "+especie["idspinvasora__idtaxon__especie"],"id":id,"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

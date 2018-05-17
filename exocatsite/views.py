# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
from django.db.models import Q
from exocatsite.models import *#Grup,Grupespecie,Viaentrada,Viaentradaespecie,Estatus,Especieinvasora,Taxon,Nomvulgar,Nomvulgartaxon,Habitat,Habitatespecie,Regionativa,Zonageografica,Imatges,Imatge
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.gis.geos import GEOSGeometry
import json, urllib, datetime
from forms import *
from models import *


#Pagina a cargar cuando se entra en la raiz
def index(request):
    return HttpResponseRedirect('/base_dades/')


# Base de dades per consultar especies
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
    regions= Zonageografica.objects.all().order_by("nom") #.distinct("nom")
    resultado=[]
    for regio in regions:
        resultado.append({'id':str(regio.id),'nom': regio.nom})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

#DATATABLES
def json_taula_especies(request):
    especies= Especieinvasora.objects.all().order_by("idtaxon__genere").values("id","idtaxon__genere","idtaxon__especie","idtaxon__subespecie")
    resultado=[]
    for especie in especies[int(request.POST["start"]):(int(request.POST["start"])+int(request.POST["length"]))]:
        # nombre de la especie(se juntan el genere con especie y subespecie)
        id=str(especie["id"])
        genere=especie["idtaxon__genere"]
        especiestr=especie["idtaxon__especie"]
        subespeciestr = especie["idtaxon__subespecie"]
        if especiestr is not None:
            try:
                genere=genere+" "+especiestr
            except:# Ojo poner breakpoint por si especie aparece en blanco
                genere=""
        if subespeciestr is not None:
            genere = genere + " [subespecie: "+subespeciestr+" ]"

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

    resultado=json.dumps({"data":resultado,"recordsTotal":len(especies),"recordsFiltered":len(especies)})
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

    def filtro_regiones(): #OJO para utilizar el unaccent he tenido que instalarlo en la migration extensiones.py y django.contrib.postgres en el INSTALLEDAPPS
        if campos["regionativa"] is not "":
            return Q(id__in=Regionativa.objects.filter(idzonageografica__nom__unaccent__icontains=campos["regionativa"]).values("idespecieinvasora"))
            # return Q(id__in=Regionativa.objects.filter(idzonageografica=campos["regionativa"]).values("idespecieinvasora"))
        else:
            return Q(id__isnull=False)

    def filtro_vias_entrada():
        if campos["viaentrada"] is not "":
            return Q(id__in=Viaentradaespecie.objects.filter(idviaentrada__viaentrada__unaccent__icontains=campos["viaentrada"]).values("idespecieinvasora"))
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
    for especie in especies[int(request.POST["start"]):(int(request.POST["start"])+int(request.POST["length"]))]:
        # nombre de la especie(se juntan el genere con especie y subespecie)
        id=especie["id"]
        genere=especie["idtaxon__genere"]
        especiestr=especie["idtaxon__especie"]
        subespeciestr = especie["idtaxon__subespecie"]
        if especiestr is not None:
            genere=genere+" "+especiestr
        if subespeciestr is not None:
            genere = genere + " [subespecie: "+subespeciestr+" ]"

        #grupo
        grup=Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom

        # # viaentrada=Viaentradaespecie.objects.get(idespecieinvasora=especie.id).idviaentrada.viaentrada
        resultado.append({'id':id,'especie': genere,'grup':grup}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':str(especie.id),'especie': genere,'grup':grup, 'varietat':varietat, 'regionativa':regionativa, 'estatuscat':estatuscat,'viaentrada':viaentrada, 'estatushistoric':estatushistoric, 'present':present}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        #resultado.append({'id':"",'especie':"",'grup':"", 'varietat':"", 'regionativa':"", 'estatuscat':"",'viaentrada':"", 'estatushistoric':"", 'present':""}) # ,'nomsvulgars':nomsvulgars,'habitat':habitat

    resultado = json.dumps({"data": resultado, "recordsTotal": len(especies), "recordsFiltered": len(especies)})
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

        # !!!! OJO DESCOMENTAR ESTO CUANDO HAGA FALTA VER LA INFO DE LAS MASSES,Y RECOMENDABLE QUE SE EJECUTE MANUALMENTE YA QUE PUEDE TARTAR EN ESPECIES COMO EL VISON
        # !!!
        # for id_massa in id_massesaigua:
        #     try:
        #         massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
        #         nom=massa.nom
        #     except:
        #         nom="# Sense Dades #"
        #     try:
        #         massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
        #         tipus=massa.id_categor
        #     except:
        #         tipus="# Sense Dades #"
        #     try:
        #         massa = MassesAigua.objects.get(id=id_massa["id_localitzacio"])
        #         conca=ConquesPrincipals.objects.filter(id=massa.idconca).values("nom_conca").first()
        #     except:
        #         conca="# Sense Dades #"
        #
        #     massesaigua.append({"nom":nom,"tipus":tipus,"conca":conca})
        # !!!

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


    viesentrada=u""
    for via in Viaentradaespecie.objects.filter(idespecieinvasora=info["id"]):
        if viesentrada=='':
            viesentrada= viesentrada+via.idviaentrada.viaentrada
        else:
            viesentrada = viesentrada+', '+ via.idviaentrada.viaentrada

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

    documentacio=[]
    for docum in Document.objects.filter(idespecieinvasora=info["id"]).values("iddoc__titol","iddoc__nomoriginal"):
        documentacio.append({"titol":docum["iddoc__titol"],"fitxer":docum["iddoc__nomoriginal"]})

    actuacions=[]
    for actuacio in Actuacio.objects.filter(idespecieinvasora=info["id"]).values("iddoc__titol","iddoc__nomoriginal").distinct("iddoc__titol"):
        actuacions.append({"titol":actuacio["iddoc__titol"],"fitxer":actuacio["iddoc__nomoriginal"]})

    resultado=json.dumps({'id':info["id"],'genere':genere,'especie':especie,'subespecie':subespecie,'varietat':varietat,'subvarietat':subvarietat,'nomsvulgars':nomsvulgars,'grup':grup,'regionativa':regionativa,'estatushistoric':estatushistoric,'estatuscatalunya':estatuscatalunya,'viesentrada':viesentrada,'presentcatalog':presentcatalog,'observacions':observacions,'imatges':imatges_especie,'titolimatge':titolimatge,'nutm1000':nutm1000,'nutm10000':nutm10000,'ncitacions':ncitacions,'nmassesaigua':nmassesaigua,'documentacio':documentacio,'actuacions':actuacions})
    return HttpResponse(resultado, content_type='application/json;')

#
# #ESPECIES EN UN CUADRO DE 10KM(EN REALIDAD SE OBTIENE UN RECUADRO DE UN CLICK)
# def json_especies_de_cuadro(request):
#     url=request.GET["url"]
#     response=urllib.urlopen(url)
#     data = json.loads(response.read())
#     resultado=[]
#     for especie in data["features"]:
#         id=especie["properties"]["IDSPINVASORA"]
#         id_taxon=Especieinvasora.objects.values_list('idtaxon').get(id=id)[0]
#         # calcular el numero de masas de agua y el numero de utms de una especie
#         id_exoaqua = ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
#         massesaigua = []
#         nmassesaigua = 0
#
#         nutm1000 = 0
#         nutm10000 = 0
#         utms = PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
#         for utm in utms:
#             if utm["idquadricula__resolution"] == 10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
#                 nutm1000 = nutm1000 + 1
#             if utm["idquadricula__resolution"] == 1000:
#                 nutm10000 = nutm10000 + 1
#
#         if id_exoaqua:  # si existe una relacion de exoaqua-exocat de dicha especie
#             id_exoaqua = id_exoaqua[0]["id_exoaqua"]  # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
#             nmassesaigua = MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()  # Ojo mirar bien esto!!!
#
#         #
#         ncitacions=Citacions.objects.filter(idspinvasora=id).count()
#
#         dades=PresenciaSp.objects.filter(idspinvasora=id).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")
#         nom=dades[0]["idspinvasora__idtaxon__genere"]+" "+dades[0]["idspinvasora__idtaxon__especie"]
#         resultado.append({"nom":nom,"id":dades[0]["idspinvasora"],"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})
#
#     resultado = json.dumps(resultado)
#     return HttpResponse(resultado, content_type='application/json;')

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
        nom=dades[0]["idspinvasora__idtaxon__genere"]+" "+dades[0]["idspinvasora__idtaxon__especie"]
        resultado.append({"nom":nom,"id":dades[0]["idspinvasora"],"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

#ESPECIES DE UNA COMARCA( SOLO OBTENER LA GEOM DE LA COMARCA! )
def json_especies_de_comarca(request):
    url=request.GET["url"]
    response=urllib.urlopen(url)
    data = json.loads(response.read())
    resultado=[]
    codi_comarca= data["features"][0]["properties"]["codicomar"]
    geom =Comarques.objects.filter(codicomar=codi_comarca).values("geom").first()["geom"]
    filtro_geom = GEOSGeometry(geom).wkt
    geom=json_especies_de_seleccion(request,filtro_geom)
    resultado.append({"geom":geom,"filtro":filtro_geom})
    #resultado.append({"geom":geom.wkt})

    resultado = json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')


#ESPCEIES EN LOS CUADROS DE 10 KM QUE HAY EN UNA SELECCION
def json_especies_de_seleccion(request,multipoligono=False):
    if multipoligono:
        pol=multipoligono
    else:
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
    if multipoligono:
        return resultado
    else:
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')

# FORMULARI CITACIONS DE ESPECIES

# def form_citacions_especies(request):
#     form = CitacionsEspeciesForm(request.POST)
#     if form.is_valid():
#         form.save()
#         lista = request.POST[""]

# FORMULARIOS DEL USUARIO
@login_required(login_url='/login/')
def view_formularis_usuari(request):
    formularios = []
    if request.user.groups.filter(name="Admins"):
        for form in CitacionsEspecie.objects.all():
            formularios.append(form)
    else:
        for form in CitacionsEspecie.objects.filter(usuari=request.user.username):
            formularios.append(form)

    context = {'formularis': formularios, 'titulo': "FORMULARIS USUARI", 'usuari': request.user.username}
    return render(request, 'exocat/formularis.html', context)

# Formulario de citacions/noves localitats de especies
@login_required(login_url='/login/')
def view_formularis_localitats_especie(request):
    ids_imatges=""
    id_form=""
    usuari = request.user.username
    nuevo="1"
    admin=False
    if request.method == 'POST':
        if request.user.groups.filter(name="Admins"):
            admin=True

        try:
            id_form=request.POST["id_form"]
            instance = get_object_or_404(CitacionsEspecie, id=id_form)
            # form = CitacionsEspeciesForm(instance=instance)
            for img in ImatgesCitacions.objects.filter(id_citacio_especie=request.POST["id_form"]).values("id"):
                ids_imatges=ids_imatges+str(img["id"])+","
        except:
            instance = None
            #nuevo = "1"
            #form = CitacionsEspeciesForm

        # QUE TIPO DE FORMULARIO ES:
        if instance is None:# Si se guarda por primera vez el form
            form = CitacionsEspeciesForm(request.POST)
        else:
            if "cargar_form" in request.POST: # Si solo se carga el form
                form = CitacionsEspeciesForm(instance=instance)
                nuevo="0"
            else:#Si se modifica un form ya existente
                form = CitacionsEspeciesForm(request.POST, instance=instance)
                nuevo="0"
        ###

        if form.is_valid() and "cargar_form" not in request.POST: # Si se envia un id_form quiere decir que se esta cargando un proyecto,no hay que guardarlo
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            camps_obligatoris = ['idspinvasora','data','NIP']
            formulario_clean  = form.cleaned_data

            if formulario_clean["idspinvasora"] == "00000":
                camps_obligatoris.append("especie")

            # Segun el tipo de corrdenadas que nos de el usuario,haremos obligatorios ciertos inputs
            if request.POST["tipus_coordenades"] == "1":
                camps_obligatoris.append("utmx")
                camps_obligatoris.append("utmy")
                camps_obligatoris.append("utmz")
            else:
                if request.POST["tipus_coordenades"] == "2":
                    camps_obligatoris.append("utm_10")
                else:
                    if request.POST["tipus_coordenades"] == "3":
                        camps_obligatoris.append("utm_1")
            #
            # Verificamos que el usuario haya dado las imagenes necesarias
            if request.POST["ids_imatges"] != "":
                ids_imatges = request.POST["ids_imatges"]
                imatges = request.POST["ids_imatges"].split(",")
                if len(imatges) < 7:
                    errorcount = "Faltan "+str(7-len(imatges))+" imatges."
                    form.add_error(None,errorcount)
            else:
                form.add_error(None,"No has penjat cap imatge.")

            # if request.POST["espai_natural_protegit"] == "si":
            #     if request.POST["tipus_espai_natural_protegit"] != "altres":
            #         form.add({"espai_natural_protegit":request.POST["tipus_espai_natural_protegit"]})
            if request.POST["autoritzacio"] != "on":
                form.add_error(None,"No has acceptat les condicions.")

            for key in camps_obligatoris:
                if not formulario_clean[key] or formulario_clean[key] == '':
                    form.add_error(key,"Aquest camp està buit")

            if form.is_valid(): # Validamos otra vez el formulario para saber si antes tenia errores
                form = form.save(commit=False) # Ojo esto es importante para modificar los campos del forma antes de guardar
                if formulario_clean["idspinvasora"] == "00000":
                    form.validat = "NO"
                else:
                    if request.user.groups.filter(name="Admins"):
                        form.validat = "SI"
                    else:
                        form.validat = "NO"

                form.usuari=usuari
                #
                if nuevo=="1":
                    form.data_creacio=datetime.date.today().strftime('%d-%m-%Y')
                form.data_modificacio=datetime.date.today().strftime('%d-%m-%Y')
                #
                new_form = form.save()
                for imatge in imatges:
                    if imatge != "":
                        img = ImatgesCitacions.objects.get(id=imatge)
                        img.id_citacio_especie = CitacionsEspecie.objects.get(id=form.id)
                        img.save()
                # nuevo="0"

                return HttpResponseRedirect('/formularis/')




            # raise form.ValidationError("You didn't fill in the {} form".format(key))
            #jemplo de envio de correo
            # subject = form.cleaned_data['subject']
            # message = form.cleaned_data['message']
            # sender = form.cleaned_data['sender']
            # cc_myself = form.cleaned_data['cc_myself']
            #
            # recipients = ['info@example.com']
            # if cc_myself:
            #     recipients.append(sender)
            #
            # send_mail(subject, message, sender, recipients)
            # return HttpResponseRedirect('/thanks/')
    else:
        form = CitacionsEspeciesForm

    especies= Especieinvasora.objects.all().order_by("idtaxon__genere").values("id", "idtaxon__genere", "idtaxon__especie")
    context={'form':form,'especies':especies,'ids_imatges':ids_imatges,'nuevo':nuevo,'id_form':id_form}
    return render(request,'exocat/formularis_localitats_especie.html',context)

# Formulario de ACA para las citacions
@login_required(login_url='/login/')
def view_formularis_aca(request):
    if request.method == 'POST':
        form = CitacionsACAForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    else:
        form = CitacionsACAForm()
    context={'form':form}
    return render(request,'exocat/formularis_aca.html',context)

@login_required(login_url='/login/')
def view_upload_imatge_citacions_especie(request):

    if request.GET:
    # def get(self, request):
        lista = []
        imatges = request.GET["ids_imatges"].split(",")
        for imatge in imatges:
            if imatge != "":
                img = ImatgesCitacions.objects.get(id=imatge)
                lista.append({'name': img.fitxer.name, 'url': img.fitxer.url, 'id': img.id})
        return JsonResponse(lista,safe=False)
        # return render(self.request, 'exocat/formularis_localitats_especie.html', {'imatges':lista})

    if request.POST:
    # def post(self, request):
        form = ImatgesCitacionsEspecieForm(request.POST, request.FILES)
        tipo_ext = ['image']
        # 2.5MB - 2621440
        # 5MB - 5242880
        # 10MB - 10485760
        # 20MB - 20971520
        # 50MB - 5242880
        # 100MB 104857600
        # 250MB - 214958080
        # 500MB - 429916160
        max_file_size = 5242880

        data = {}
        if form.is_valid():
            imagen = form.cleaned_data["fitxer"]
            # comprobar extension:
            if (imagen.content_type.split('/')[0] not in tipo_ext):
                data = {"is_valid": False, 'errormessage': 'Error: El fitxer ha de ser una imatge.'}
            # comprobar tamaño:
            else:
                if (imagen._size > max_file_size):
                    data = {"is_valid": False, 'errormessage': 'Error: El tamany del fixter ha de ser menor a 5MB.'}
                else:
                    imatge = form.save()
                    data = {'is_valid':True, 'name': imatge.fitxer.name , 'url': imatge.fitxer.url, 'id':imatge.id }
        else:
            data = {"is_valid":False, 'errormessage':'Error al pujar la imatge.'}
        return JsonResponse(data)

@login_required(login_url='/login/')
def json_taula_formularis_usuari(request):
    formularios=[]
    nom_especie = ""
    if request.user.is_authenticated():
        formscitacions=[]
        if request.user.groups.filter(name="Admins"):
            formscitacions=CitacionsEspecie.objects.all().values("id","especie","idspinvasora","usuari","validat","data_creacio","data_modificacio")
        else:
            formscitacions = CitacionsEspecie.objects.filter(usuari=request.user.username).values("id","especie","idspinvasora","usuari","validat","data_creacio","data_modificacio")

        for form in formscitacions:
            try:
                if form["idspinvasora"]=="00000":
                    nom_especie=form["especie"]
                else:
                    #especies= Especieinvasora.objects.all().order_by("idtaxon__genere").values("id", "idtaxon__genere", "idtaxon__especie")
                    especie=Especieinvasora.objects.filter(id=form["idspinvasora"]).values("id", "idtaxon__genere", "idtaxon__especie")
                    nom_especie=especie[0]["idtaxon__genere"]+" "+especie[0]["idtaxon__especie"]
            except:
                nom_especie=""

            formularios.append({"id":form["id"],"especie":nom_especie,"usuari":form["usuari"],"validat":form["validat"],"data_creacio":form["data_creacio"],"data_modificacio":form["data_modificacio"]})

    resultado = json.dumps(formularios)
    return HttpResponse(resultado, content_type='application/json;')
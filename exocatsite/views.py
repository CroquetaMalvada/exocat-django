# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
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
from itertools import chain
import json, urllib, datetime, os, requests, codecs, csv, unicodecsv
#para generar un excel
try:
    import cStringIO as StringIO
except:
    import StringIO
#from xlsxwriter.workbook import Workbook
from openpyxl import  Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook #util para el httpresponse
#Tuto de openpyxl en https://medium.com/aubergine-solutions/working-with-excel-sheets-in-python-using-openpyxl-4f9fd32de87f
#
from forms import *
from models import *


from django.db.models.functions import Substr

import unicodecsv as csv # instalado con el pip ya que el csv a secas no incluye unicode
from io import BytesIO
#import csv,io


def dictfetchall(cursor):
    # Devuelve todos los campos de cada row como una lista
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

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
def json_select_varietat(request):# Ojo la varietat no esta en un tabla aparte,la extraigo de los taxons y le hago un distinct(esto puede quedar feo si se anaden muchos y con nombres similares)
    varietats= Taxon.objects.filter(varietat__isnull = False).values("varietat").order_by("varietat").distinct("varietat")
    resultado=[]
    for vari in varietats:
        resultado.append({'varietat': vari["varietat"]})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

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

# def json_select_estatus(request):
#     estatus= Estatus.objects.all().order_by("nom")
#     resultado=[]
#     for estat in estatus:
#         resultado.append({'id':str(estat.id),'nom': estat.nom})
#     resultado=json.dumps(resultado)
#     return HttpResponse(resultado, content_type='application/json;')
def json_select_estatus_cat(request):
    estatus= Estatus.objects.filter(estatus_catalunya = True).order_by("nom")
    resultado=[]
    for estat in estatus:
        resultado.append({'id':str(estat.id),'nom': estat.nom})
    resultado=json.dumps(resultado)
    return HttpResponse(resultado, content_type='application/json;')

def json_select_estatus_historic(request):
    estatus= Estatus.objects.filter(estatus_historic = True).order_by("nom")
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
    ids_especies=[]
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
        #     varietat = varietat+' ", '+str(especie.idtaxon.subvarietat)
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

    # para el input de ids para el csv
    for especie in especies:
        ids_especies.append(especie["id"])
    ids=""
    if(len(ids_especies)>0):
        ids = ','.join(ids_especies)

    resultado=json.dumps({"data":resultado,"recordsTotal":len(especies),"recordsFiltered":len(especies),"ids_especies":ids,"num_elem":len(ids_especies)})
    return HttpResponse(resultado, content_type='application/json;')

# LOS FILTROS A SECAS
def filtrar_especies(campos):

    ###########ESPECIES QUE TIENEN CITACIONES QUE CUMPLAN LO MANDADO EN LOS FILTROS
    list_especies =[]
    list_espceis_citacions=[]
    if campos["data_min_citacio"] is not "" or campos["data_max_citacio"] is not "":
        data_min=0
        data_max=0
        if campos["data_min_citacio"] is "":
            data_min=0
        else:
            data_min=int(campos["data_min_citacio"])
        if campos["data_max_citacio"] is "":
            data_max=9999
        else:
            data_max=int(campos["data_max_citacio"])
        if data_max-data_min>0:#comprobar que no hayan metido una fecha min mayor que la max
            ####CITACIONES ANTIGUAS
            citacions = Citacions.objects.exclude(Q(data__icontains="Indeterminada") | Q(data__isnull=True) | Q(data="")).values("id","idspinvasora","data")
            for citacio in citacions:
                try:
                    #if campos["data_min_citacio"] is not "":#
                    # any = int(citacio["data"][-4:])
                    esint = int(citacio["data"])
                    any=0
                    any_min = 9999
                    any_max = -1
                    for year in  range(1980,datetime.date.today().year+1):
                        if(citacio["data"].find(str(year))!=-1):# si encuentra x any en el string de data
                            if year < any_min:
                                any_min = year
                            if year > any_max:
                                any_max = year
                        #any = int(citacio["data"][-4:])
                    if(any_min!=9999 and any_max!=-1):
                        #if(citacio["idspinvasora"]=="Agav_amer"):
                         #   None
                        if((any_min>data_min and data_max==9999) or (data_min==0 and any_max<data_max)) or (any_min>data_min and any_max<data_max):
                            list_especies.append(citacio["idspinvasora"])
                            #list_citacions.append({"id":citacio["id"],"especie":citacio["idspinvasora"],"data":citacio["data"]})
                            #citacions.exclude(id=citacio["id"])
                except:
                    None

            ####CITACIONES DE FORMULARIO
            citacions = CitacionsEspecie.objects.all().values("id","idspinvasora","data")
            for citacio in citacions:
                any=0;
                for year in range(1980, datetime.date.today().year+1):
                    if (citacio["data"].find(str(year)) != -1):
                        any=year
                        break
                if((any>data_min and data_max==9999) or (data_min==0 and any<data_max)):
                    list_especies.append(citacio["idspinvasora"])

    list_especies_citacions=set(list_especies)#hacemos un "distinct" a la lista de especies para limpiarla

    #list_espceis_citacions = set([citacio.idspinvasora for citacio in list_citacions])
    # CREAMOS LOS FILTROS:
    estatus = Estatus.objects.all().values("id") #lo metemos en una variable ya que esta lista la usaremos en mas de una ocasion en los filtros

    def filtro_nombre():
        if campos["especie"] is not "":
            for especie in campos["especie"].split(" "):
                return (Q(idtaxon__genere__icontains=especie) | Q(idtaxon__especie__icontains=especie) | Q (idtaxon__subespecie__icontains=especie) | Q(idtaxon__varietat__icontains=especie))
        else:
            return Q(id__isnull=False)

    def filtro_genere():
        if campos["genere"] is not "":
            return (Q(idtaxon__genere__icontains=campos["genere"]))
        else:
            return Q(id__isnull=False)

    def filtro_especie():
        if campos["especie"] is not "":
            return (Q(idtaxon__especie__icontains=campos["especie"]))
        else:
            return Q(id__isnull=False)

    def filtro_subespecie():
        if campos["subespecie"] is not "":
            return (Q(idtaxon__subespecie__icontains=campos["subespecie"]))
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

    def filtro_regio_nativa(): #OJO para utilizar el unaccent he tenido que instalarlo en el psql del servidor(como usuario psotgres) y django.contrib.postgres en el INSTALLEDAPPS
        if campos["regionativa"] is not "":
            return Q(regio_nativa__unaccent__icontains=campos["regionativa"])
        else:
            return Q(id__isnull=False)
    # def filtro_regiones(): #OJO para utilizar el unaccent he tenido que instalarlo en la migration extensiones.py y django.contrib.postgres en el INSTALLEDAPPS
    #     if campos["regionativa"] is not "":
    #         return Q(id__in=Regionativa.objects.filter(idzonageografica__nom__unaccent__icontains=campos["regionativa"]).values("idespecieinvasora"))
    #         # return Q(id__in=Regionativa.objects.filter(idzonageografica=campos["regionativa"]).values("idespecieinvasora"))
    #     else:
    #         return Q(id__isnull=False)

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

    def filtro_reglamento_eur():
        if campos["present_reglament_eur"] is not "":
            return Q(reglament_ue=campos["present_reglament_eur"])
        else:
            return Q(id__isnull=False)

    def filtro_data_citacions():
        # if campos["data_min_citacio"] is not "":
        #     for citacio in Citacions.objects.filter()
        #     return True
        #if Q(id__in=list_espceis_citacions):
        if campos["filtrar_data_citacions"] == "true":
            return Q(id__in=list_especies_citacions)
        else:
            return Q(id__isnull=False)
        #else:
         #   return Q(id__isnull=False)
            #if not Citacions.objects.filter(str(data[-2])>=campos["data_min_citacio"])

    # APLICAMOS LOS FILTROS:

    especies= Especieinvasora.objects.filter(
        # para el nombre(campo especie) !Ojo __icontains no es sensible a mayusculas a diferencia de __contains!
        filtro_nombre(),# incluye el genere,especie,subespecie y varietat
        # filtro_genere(),
        # filtro_especie(),
        # filtro_subespecie(),
        # filtro_varietat(),

        #para los grups
        filtro_grups(),

        #para estatus catalunya
        filtro_estatus_cat(),



        # para las regiones nativas
        filtro_regio_nativa(),
        # filtro_regiones(),

        # para las vias de entrada
        filtro_vias_entrada(),

        # para el estatus historico
        filtro_estatus_historico(),

        # para el present al catalogo
        filtro_catalogo(),

        # para el present al reglamento europeo
        filtro_reglamento_eur(),

        # para las fechas de citaciones
        filtro_data_citacions(),

    ).order_by("idtaxon__genere").values("id","idtaxon__genere","idtaxon__especie","idtaxon__subespecie")

    return especies

#ESPECIES FILTRADAS
def json_taula_especies_filtres(request):
    campos=request.POST
    especies = filtrar_especies(campos)
    # FINALMENTE DEVOLVEMOS CADA ESPECIE QUE HAYA PASADO LOS FILTROS:
    resultado = []
    ids_especies = []
    try:
        for especie in especies[int(request.POST["start"]):(int(request.POST["start"]) + int(request.POST["length"]))]:
            # nombre de la especie(se juntan el genere con especie y subespecie)
            id = especie["id"]
            genere = especie["idtaxon__genere"]
            especiestr = especie["idtaxon__especie"]
            subespeciestr = especie["idtaxon__subespecie"]
            if especiestr is not None:
                genere = genere + " " + especiestr
            if subespeciestr is not None:
                genere = genere + u" [Subespècie: " + subespeciestr + " ]"

            # grupo
            grup = Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom

            resultado.append({'id': id, 'especie': genere, 'grup': grup})  # ,'nomsvulgars':nomsvulgars,'habitat':habitat
        # para el input de ids para el csv
        for especie in especies:
            ids_especies.append(especie["id"])
        ids=""
        if(len(ids_especies)>0):
            ids = ','.join(ids_especies)
        resultado = json.dumps({"data": resultado, "recordsTotal": len(especies), "recordsFiltered": len(especies), "ids_especies":ids,"num_elem":len(ids_especies)})
        return HttpResponse(resultado, content_type='application/json;')

    except:
        resultado = []
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')


# GENERAR CSV DE ESPECIES FILTRADAS
def generar_csv_especies(request):
    # f = BytesIO()
    # w = csv.writer(f, encoding='utf-8')
    # _ = w.writerow([u'ést', u'ñgfdgdf'])
    # _ = f.seek(0)
    # r = csv.reader(f, encoding='utf-8')
    # next(r) == [u'é', u'ñ']
    #buffer = io.BytesIO()
    #writer = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    #writer.writerow([u'Taxon', u'Grup', u'Regio nativa', u'Vies d"entrada', u'Estatus general', u'Estatus Catalunya',u'Present al "Catalogo"', u'Present al Reglament Europeu'])
    #writer.writerow({'id','NAME','ABBREVIATION','ADDRESS'})
    especies = request.POST["ids_especies_filtradas"]
    resultado = HttpResponse(content_type='text/csv')
    resultado['Content-Disposition'] = 'attachment; filename="EspeciesFiltrades.csv"'

    writer = csv.writer(resultado, delimiter=str(u';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    resultado.write(u'\ufeff'.encode('utf8')) # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'Taxon', u'Grup', 'Regió nativa', u"Vies d'entrada", u'Estatus general', u'Estatus Catalunya',u'Present al "Catálogo"', u'Present al Reglament Europeu'])

    cursor = connection.cursor()
    try:
        if 'DELETE' in especies or 'delete' in especies or 'UPDATE' in especies or 'update' in especies:# toda precaucion con las querys es poca
            raise Http404('Error al generar el csv.')
        especies = especies.split(",")
        cursor.execute("SELECT  CONCAT_WS(' ',taxon.genere, taxon.especie) AS taxon,"
        " taxon.subespecie AS subespecie,"
        " grup.nom AS grup,"
        " especieinvasora.regio_nativa AS regionativa,"
        " (SELECT string_agg(viaentrada.viaentrada,',') FROM viaentradaespecie INNER JOIN viaentrada ON viaentrada.id = viaentradaespecie.idviaentrada WHERE viaentradaespecie.idespecieinvasora = especieinvasora.id) AS viesentrada,"
        " (SELECT nom FROM estatus WHERE id=especieinvasora.idestatushistoric) AS estatushistoric,"
        " (SELECT nom FROM estatus WHERE id=especieinvasora.idestatuscatalunya) AS estatuscatalunya,"
        " (SELECT CASE WHEN especieinvasora.present_catalogo='N' THEN 'No' ELSE 'Si' END AS presentcatalog) AS presentcatalog,"
        " (SELECT CASE WHEN especieinvasora.reglament_ue='N' THEN 'No' ELSE 'Si' END AS presentreglamenteur) AS presentreglamenteur"
        " FROM especieinvasora"
        " INNER JOIN taxon ON especieinvasora.idtaxon = taxon.id" 
        " INNER JOIN grupespecie ON especieinvasora.id = grupespecie.idespecieinvasora"
        " INNER JOIN grup ON grup.id = grupespecie.idgrup"
        " WHERE especieinvasora.id = ANY( %s ) ORDER BY taxon",[especies])
        fetch = dictfetchall(cursor)

        for especie in fetch:
            writer.writerow([especie["taxon"], especie["grup"], especie["regionativa"], especie["viesentrada"], especie["estatushistoric"], especie["estatuscatalunya"], especie["presentcatalog"],especie["presentreglamenteur"]])
        return resultado
    except:
        raise Http404('Error al generar el csv.')

    finally:
        cursor.close()


#GENERAR UNA PLANTILLA CSV PARA LA INTRODUCCION DE CITACIONES
def generar_csv_plantilla_citaciones(request):
    # f = BytesIO()
    # w = csv.writer(f, encoding='utf-8')
    # _ = w.writerow([u'ést', u'ñgfdgdf'])
    # _ = f.seek(0)
    # r = csv.reader(f, encoding='utf-8')
    # next(r) == [u'é', u'ñ']
    #buffer = io.BytesIO()
    #writer = csv.writer(buffer, quoting=csv.QUOTE_ALL)
    #writer.writerow([u'Taxon', u'Grup', u'Regio nativa', u'Vies d"entrada', u'Estatus general', u'Estatus Catalunya',u'Present al "Catalogo"', u'Present al Reglament Europeu'])
    #writer.writerow({'id','NAME','ABBREVIATION','ADDRESS'})
    #writer.writerow([u'\/Obligatori\/', u'\/', '\/', u'\/Obligatori un dels 3\/', u'\/', u'',u'', u'', u'', u'\/Obligatori\/', u'\/Obligatori\/', ''])
    if request.POST["tipo"]=="1": # SI ES UN EXCEL
        #----------------- intento 1
        # output = StringIO.StringIO()
        #
        # book = Workbook(output)
        # sheet = book.add_worksheet("citacions")
        # sheet.write(u'ESPÈCIE', u'COORDENADA UTM-X', u'COORDENADA UTM-Y', u"UTM 1 KM", u'UTM 10 KM', u'localitat',u'municipi', u'comarca', u'provincia', u'DATA', u'AUTOR/S', 'observacions')
        # book.close()
        #
        # output.seek(0)
        # resultado = HttpResponse(content_type='application/vnd.ms-excel')
        # resultado['Content-Disposition'] = 'attachment; filename="PlantillaCitacions.xlsx"'
        # workbook = Workbook(resultado)
        # worksheet = workbook.add_worksheet()
        #
        # worksheet.write('A1', 'Hello world')
        #
        # #workbook.close()
        # return resultado
        # ----------------- intento 2
        # output = BytesIO()
        #
        # workbook = Workbook(output, {'in_memory': True})
        # worksheet = workbook.add_worksheet()
        # # + Info en https://xlsxwriter.readthedocs.io/worksheet.html
        # worksheet.write(0, 0, u'ESPÈCIE')
        # worksheet.write(0, 1, u'COORDENADA UTM-X')
        # worksheet.write(0, 2, u'COORDENADA UTM-Y')
        # worksheet.write(0, 3, u'UTM 1 KM')
        # worksheet.write(0, 4, u'UTM 10 KM')
        # worksheet.write(0, 5, u'localitat')
        # worksheet.write(0, 6, u'municipi')
        # worksheet.write(0, 7, u'comarca')
        # worksheet.write(0, 8, u'provincia')
        # worksheet.write(0, 9, u'DATA')
        # worksheet.write(0, 10, u'AUTOR/S')
        # worksheet.write(0, 11, u'observacions')
        # workbook.close()
        #
        # output.seek(0)
        #
        # response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        # response['Content-Disposition'] = "attachment; filename=PlantillaCitacions.xlsx"
        #
        # output.close()
        #
        # return response
        # ----------------- intento 3
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.append([u'ESPÈCIE', u'COORDENADA UTM-X', u'COORDENADA UTM-Y', u"UTM 1 KM", u'UTM 10 KM', u'localitat',u'municipi', u'comarca', u'provincia', u'DATA', u'AUTOR/S', 'observacions'])
        response = HttpResponse(content=save_virtual_workbook(workbook), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=PlantillaCitacions.xlsx'
        return response

    else: # SI ES UN CSV
        resultado = HttpResponse(content_type='text/csv')
        resultado['Content-Disposition'] = 'attachment; filename="PlantillaCitacions.csv"'

        writer = csv.writer(resultado, delimiter=str(";"), dialect='excel') #  quoting=csv.QUOTE_ALL,writer = csv.writer(resultado, delimiter=str(';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
        resultado.write(u'\ufeff'.encode('utf8')) # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
        writer.writerow([u'ESPÈCIE', u'COORDENADA UTM-X', u'COORDENADA UTM-Y', u"UTM 1 KM", u'UTM 10 KM', u'localitat',u'municipi', u'comarca', u'provincia', u'DATA', u'AUTOR/S', 'observacions'])#, "*Nota: Els camps en majúscules son obligatoris. Excepte els de les UTM's ja que només serà necessari omplir un dels 3."
        #writer.writerow([u'CAMPS OBLIGATORIS:',u'Espècie', u'(Opció 1)Coordenada UTM-X', u'(Opció 1)Coordenada UTM-Y', u"(Opció 2)UTM 1km", u'(Opció 3)UTM 10km', u'Data', u'Autor/s', u'',u'CAMPS OPCIONALS:',u'Localitat',u'Municipi', u'Comarca', u'Provincia', 'Observacions'])
        return resultado
    return []

#UPLOAD CITACIONES EN CSV
def upload_citaciones_csv(request):
    resultado = []
    errores=0
    errorlist=[]
    lineas_error_especie=""
    lineas_error_coordenadas = ""
    lineas_error_data = ""
    lineas_error_autor = ""
    nlinea=0
    # try:
    #     csvfile = request.FILES['csv_file']
    #     dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "latin-1").read(1024))
    #     csvfile.open()
    #     reader = csv.reader(codecs.EncodedFile(csvfile, "latin-1"), delimiter=str(";"), dialect=dialect)
    # except:
    #     try:
    #         csvfile = request.FILES['csv_file']
    #         dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
    #         csvfile.open()
    #         reader = csv.reader(codecs.EncodedFile(csvfile, "utf-8"), delimiter=str(","), dialect=dialect)
    #     except:
    #         return JsonResponse({"error": True, 'errormessage': 'Error: Hi han caracters incompatibles dintre del fitxer.'})

    # try:
    if request.POST:
        file= request.FILES['fitxer']
        tipo=0; #1=excel xlsx 2=csv
        # if not file.name.endswith(".csv"):
        #     return JsonResponse({"error": True, 'errormessage': 'Error: El fitxer ha de ser un ".CSV"'})
        #
        # decoded_file = file.read().decode('utf-8')
        # lines=decoded_file.split("\n")

        #### Primero averiguamos el tipo de fixhero que es
        if not file.name.endswith(".xlsx"):
            if not file.name.endswith(".csv"):
                return JsonResponse({"error": True, 'errores': 'Error: El fitxer ha de ser un ".CSV"'})
            else:
                tipo=2
        else:
            tipo=1
        #############
        ##Ahora,segun el tipo de archivo lo leemos
        if tipo==1:
            reader=load_workbook(file.name)
            sheet=reader.active
            # b1=sheet['B1']
            # b2 = sheet['B2']
            reader=sheet
        if tipo==2:
            try:
                reader=unicodecsv.reader(file, encoding='utf8', delimiter=str(';'))#, encoding='latin-1', delimiter=str('\t')
                #reader=unicodecsv.reader(file, encoding='utf-8', delimiter=str(csv.Sniffer().sniff(file.read(1024)).delimiter))#, encoding='latin-1', delimiter=str('\t')

            except:
                reader = unicodecsv.reader(file, encoding='latin-1', delimiter=str(';'))
            #reader=unicodecsv.reader(file, encoding='latin-1', delimiter=str(csv.Sniffer().sniff(file.read(1024)).delimiter))#, encoding='latin-1', delimiter=str('\t')
        #reader=unicodecsv.reader(request.FILES['fitxer'], encoding='latin-1', delimiter=str(','))#, encoding='latin-1', delimiter=str('\t')
        # if not reader.dialect.delimiter=="\t":
        #     return JsonResponse({"error": True, 'errores': 'Error: Hi han caracters incompatibles dintre del fitxer.'})
        for line in reader: #Miramos todas las lineas en busca de errores
            if nlinea>0:#Evitamos analizar la primera linea
                # fields=line.split(str("\t"))
                # data_dict = {}
                if tipo == 1:
                    especie = line[0].value
                    utmx = line[1].value
                    utmy = line[2].value
                    utm1 = line[3].value
                    utm10 = line[4].value
                    localitat = line[5].value
                    municipi = line[6].value
                    comarca = line[7].value
                    provincia = line[8].value
                    data = line[9].value
                    autor = line[10].value
                    observacions = line[11].value
                else:
                    especie=line[0]
                    utmx=line[1]
                    utmy=line[2]
                    utm1=line[3]
                    utm10=line[4]
                    localitat=line[5]
                    municipi=line[6]
                    comarca=line[7]
                    provincia=line[8]
                    data=line[9]
                    autor=line[10]
                    observacions=line[11]

                #####COMPROBAR QUE ESTEN LOS CAMPOS OBLIGATORIOS
                #Especie
                if especie =="" or especie is None:
                    errores+=1
                    lineas_error_especie+=str(nlinea+1)+' ", '
                    #lineas_error_especie.append(nlinea+1)
                    #errorlist.append("El camp 'Espécie' està buit o es incorrecte.")
                #Comprobar que al menos uno de los de coordenadas tenga algo
                if utmx=="" or utmy=="" or utmx is None or utmy is None:
                    if utm1=="" or utm1 is None:
                        if utm10=="" or utm10 is None:
                            errores+=1
                            lineas_error_coordenadas+=str(nlinea+1)+' ", '
                            #lineas_error_coordenadas.append(nlinea + 1)
                            #errorlist.append("Es obligatori posar al menys un del 3 tipus de coordenades.")
                #Data
                if data =="" or data is None:
                    errores += 1
                    lineas_error_data+=str(nlinea+1)+' ", '
                    #lineas_error_data.append(nlinea + 1)
                    #errorlist.append("El camp 'Data' està buit o es incorrecte.")
                else:
                    errodata=0
                    try:
                        data=datetime.datetime.strptime(data, '%d-%m-%Y') #no hace falta quitar lo del time porque esto es solo para comprovar que este bien escrito
                    except:
                        try:
                            data=datetime.datetime.strptime(data, '%Y-%m-%d')
                            data = datetime.datetime.strptime(data, '%d-%m-%Y')
                        except:
                            errores+=1
                            lineas_error_data+=str(nlinea+1)+' ", '
                            #lineas_error_data.append(nlinea + 1)
                            #errorlist.append("El format del camp 'Data' es incorrecte.")
                #Autor
                if autor=="" or autor is None:
                    errores+=1
                    lineas_error_autor+=str(nlinea+1)+' ", '
                    #lineas_error_autor.append(nlinea + 1)
                    #errorlist.append("El camp 'Autor/s' està buit o es incorrecte.")

            nlinea+=1
        #Ahora anadimos el error general de cada campo si hay lineas de fallo en el mismo
        if lineas_error_especie != "":
            errorlist.append("El camp <b>'Espécie'</b> està buit o es incorrecte en les següents línies: <hr>"+'" '+lineas_error_especie)
        if lineas_error_coordenadas != "":
            errorlist.append("Error de coordenades en les següents línies: <hr>"+'" '+lineas_error_coordenadas)
        if lineas_error_data != "":
            errorlist.append("El camp <b>'Data'</b> està buit o té un format incorrecte(recomenable posar 'dia-mes-any') en les següents línies: <hr>"+'" '+lineas_error_data)
        if lineas_error_autor != "":
            errorlist.append("El camp <b>'Autor/s'</b> està buit o es incorrecte en les següents línies: <hr>"+'" '+lineas_error_especie)


        #decoded_file = file.read().decode('utf-8').splitlines()
        #reader = csv.DictReader(decoded_file)

        # for row in reader:
        #     row[0]
        #     resultado = {"error": True, 'errormessage': 'Error: El fitxer ha de ser una imatge.'}

    # except:
    #     return JsonResponse({"error": True, 'errormessage': "Error: Hi hagut un problema al llegir l'arxiu."})
    #return JsonResponse(resultado)
    try:
        resultado = {"errores":errores,"listado_errores":errorlist}
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')
    except:
        return []

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
    citacions= Citacions.objects.filter(idspinvasora=id,geom_4326__isnull = False).values("citacio","localitat","municipi","comarca","provincia","data","autor_s","font")
    ncitacions = citacions.count()
    #Ahora las citaciones "nuevas"
    ncitacions = ncitacions + CitacionsEspecie.objects.filter(idspinvasora=id, utmx__isnull=False, utmy__isnull=False, validat="SI").values("utmx").distinct().count()
    # ncitacions = Citacions.objects.filter(idspinvasora=id,geom_4326__isnull = False).count()

    # calcular el numero de masas de agua y el numero de utms de una especie
    id_exoaqua= ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
    massesaigua = []
    nmassesaigua=0

    nutm1000=0
    nutm10000=0

    nutm10000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=10000).values("idquadricula").distinct().count()
    nutm1000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=1000).values("idquadricula").distinct().count()
    ###Ahora sumar las utms "nuevas"
    nutm10000 = nutm10000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_10__isnull=False, validat="SI").values("utm_10").distinct().count()
    nutm1000 = nutm1000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_1__isnull=False, validat="SI").values("utm_1").distinct().count()
    ###
    # utms10000= PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
    # for utm in utms:
    #     if utm["idquadricula__resolution"]==10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
    #         nutm10000=nutm10000+1
    #     if utm["idquadricula__resolution"]==1000:
    #         nutm1000 = nutm1000 + 1



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
    regionativa=Especieinvasora.objects.get(id=info["id"]).regio_nativa
    if regionativa==None:
        regionativa=""
    # regionativa=u""
    # try:# hacemos try porque hay algunos en los que es nulo(?) y peta
    #     for reg in Regionativa.objects.filter(idespecieinvasora=info["id"]):
    #         if reg == '':
    #             regionativa = regionativa + reg.idzonageografica.nom
    #         else:
    #             regionativa = regionativa + ', ' + reg.idzonageografica.nom
    #
    #     # regionativa=Regionativa.objects.get(idespecieinvasora=info["id"]).idzonageografica.nom
    # except:
    #     regionativa=""#"Desconeguda"

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

    presentreglamenteur=Especieinvasora.objects.get(id=info["id"]).reglament_ue
    if presentreglamenteur=="S":
        presentreglamenteur="Si"
    else:
        presentreglamenteur="No"

    observacions=Especieinvasora.objects.get(id=info["id"]).observacions
    if observacions==None:
        observacions=""

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

    resultado=json.dumps({'id':info["id"],'genere':genere,'especie':especie,'subespecie':subespecie,'varietat':varietat,'subvarietat':subvarietat,'nomsvulgars':nomsvulgars,'grup':grup,'regionativa':regionativa,'estatushistoric':estatushistoric,'estatuscatalunya':estatuscatalunya,'viesentrada':viesentrada,'presentcatalog':presentcatalog,'presentreglamenteur':presentreglamenteur,'observacions':observacions,'imatges':imatges_especie,'titolimatge':titolimatge,'nutm1000':nutm1000,'nutm10000':nutm10000,'ncitacions':ncitacions,'nmassesaigua':nmassesaigua,'documentacio':documentacio,'actuacions':actuacions})
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
def json_especies_de_cuadro(request):# Ojo aqui no hace falta lo de las citaciones nuevas porque se las pasamos en el js
    url=request.GET["url"]
    response=urllib.urlopen(url)
    data = json.loads(response.read())
    resultado=[]
    for especie in data["features"]:
        id=especie["properties"]["IDSPINVASORA"]
        id_taxon=Especieinvasora.objects.values_list('idtaxon').get(id=id)[0]
        # calcular el numero de masas de agua y el numero de utms de una especie
        id_exoaqua = ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
        grup = Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom
        massesaigua = []
        nmassesaigua = 0

        nutm1000 = 0
        nutm10000 = 0

        nutm10000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=10000).values("idquadricula").distinct().count()
        nutm1000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=1000).values("idquadricula").distinct().count()

        ###Ahora sumar las utms "nuevas"
        nutm10000 = nutm10000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_10__isnull=False, validat="SI").values("utm_10").distinct().count()
        nutm1000 = nutm1000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_1__isnull=False, validat="SI").values("utm_1").distinct().count()
        # utms = PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
        # for utm in utms:
        #     if utm["idquadricula__resolution"] == 10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
        #         nutm10000 = nutm10000 + 1
        #     if utm["idquadricula__resolution"] == 1000:
        #         nutm1000 = nutm1000 + 1

        if id_exoaqua:  # si existe una relacion de exoaqua-exocat de dicha especie
            id_exoaqua = id_exoaqua[0]["id_exoaqua"]  # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
            nmassesaigua = MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()  # Ojo mirar bien esto!!!

        #
        ncitacions=Citacions.objects.filter(idspinvasora=id,geom_4326__isnull = False).count()
        #Ahora las citaciones "nuevas"
        ncitacions = ncitacions + CitacionsEspecie.objects.filter(idspinvasora=id, utmx__isnull=False, utmy__isnull=False, validat="SI").values("utmx").distinct().count()

        dades=PresenciaSp.objects.filter(idspinvasora=id).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")
        nom=dades[0]["idspinvasora__idtaxon__genere"]+" "+dades[0]["idspinvasora__idtaxon__especie"]
        resultado.append({"nom":nom,"id":dades[0]["idspinvasora"],"grup":grup,"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})

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
    # para que al juntar especies y especies_2 no salga 2 veces una especie que existe en ambas ponemos el exclude
    especies_2 = CitacionsEspecie.objects.filter(utm_10__isnull=False, utm_10__in=quad).exclude(idspinvasora__in=especies.values_list('idspinvasora',flat=True)).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")

    especies = list(chain(especies, especies_2))
    #Ojo  pregunta:contar tambien las especies que no se localizaron en utms pero si en una citacion?

    resultado=[]
    for especie in especies:
        id=especie["idspinvasora"]
        id_taxon = Especieinvasora.objects.values_list('idtaxon').get(id=id)[0]
        grup = Grupespecie.objects.get(idespecieinvasora=id).idgrup.nom
        # calcular el numero de masas de agua y el numero de utms de una especie
        id_exoaqua = ExoaquaToExocat.objects.filter(id_exocat=id_taxon).values("id_exoaqua")
        massesaigua = []
        nmassesaigua = 0

        nutm1000 = 0
        nutm10000 = 0

        nutm10000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=10000).values("idquadricula").distinct().count()
        nutm1000= PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=1000).values("idquadricula").distinct().count()

        ###Ahora sumar las utms "nuevas"
        nutm10000 = nutm10000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_10__isnull=False, validat="SI").values("utm_10").distinct().count()
        nutm1000 = nutm1000 + CitacionsEspecie.objects.filter(idspinvasora=id, utm_1__isnull=False, validat="SI").values("utm_1").distinct().count()
        ###
        # utms = PresenciaSp.objects.filter(idspinvasora=id).values("idquadricula__resolution")
        # for utm in utms:
        #     if utm["idquadricula__resolution"] == 10000: #Ojo que la resolution no indica nada de metros! si pone 10000 son de 1000m!!!
        #         nutm10000 = nutm10000 + 1
        #     if utm["idquadricula__resolution"] == 1000:
        #         nutm1000 = nutm1000 + 1

        if id_exoaqua:  # si existe una relacion de exoaqua-exocat de dicha especie
            id_exoaqua = id_exoaqua[0]["id_exoaqua"]  # en teoria solo debe devolvernos un resultado(tambien se podria usar un object get)
            nmassesaigua = MassaAiguaTaxon.objects.filter(id_taxon_exoaqua=id_exoaqua).count()  # Ojo mirar bien esto!!!

        #

        ncitacions = Citacions.objects.filter(idspinvasora=id,geom_4326__isnull = False).count()
        #Ahora las citaciones "nuevas"
        ncitacions = ncitacions + CitacionsEspecie.objects.filter(idspinvasora=id, utmx__isnull=False, utmy__isnull=False, validat="SI").values("utmx").distinct().count()
        resultado.append({"nom":especie["idspinvasora__idtaxon__genere"]+" "+especie["idspinvasora__idtaxon__especie"],"id":id,"grup":grup,"nutm1000":nutm1000,"nutm10000":nutm10000,"ncitacions":ncitacions,"nmassesaigua":nmassesaigua})
    if multipoligono:
        return resultado
    else:
        resultado = json.dumps(resultado)
        return HttpResponse(resultado, content_type='application/json;')

# GEOMETRIAS DE PUNTOS Y UTMS1X1 DE ESPECIE PARA PASARLOS A UTM10X10 EN EL JS
def json_geometries_punts(request):
    geometrias=[]
    id=request.POST["id"]
    quadriculas = [] # se usara para asegurar que no haya quadriculas repetidas
    #### citaciones pnutuales
    # antiguas
    for cit in Citacions.objects.filter(idspinvasora=id,geom_4326__isnull = False).values("geom_4326").distinct():
        for quad in Quadricula.objects.filter(geom_4326__intersects=cit["geom_4326"].wkt,resolution=10000).values("id","geom_4326").distinct("id"):
        #quad = Quadricula.objects.get(geom_4326__intersects=cit["geom_4326"].wkt,resolution=10000).values("id","geom_4326")[0]
            if quad["id"] not in quadriculas:
                quadriculas.append(quad["id"])
    # nuevas
    for cit in CitacionsEspecie.objects.filter(idspinvasora=id, utmx__isnull=False, utmy__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct():
        for quad in Quadricula.objects.filter(geom_4326__intersects=GEOSGeometry(cit["geom"], srid=4326).wkt,resolution=10000).values("id","geom_4326").distinct("id"):
            if quad["id"] not in quadriculas:
                quadriculas.append(quad["id"])

    # #### utm10x10
    # # antiguas
    # for utm in PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=10000).values("idquadricula__geom_4326").distinct("idquadricula"):
    #     for quad in Quadricula.objects.filter(geom_4326__intersects=utm["idquadricula__geom_4326"].wkt,resolution=10000).values("id","geom_4326").distinct("id"):
    #         if quad["id"] not in quadriculas:
    #             quadriculas.append(quad["id"])
    #     #geometrias.append({"geom_4326":str(utm["idquadricula__geom_4326"].wkt)})
    # # nuevas
    # for utm in CitacionsEspecie.objects.filter(idspinvasora=id, utm_10__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct("utm_10"):
    #     for quad in Quadricula.objects.filter(geom_4326__intersects=GEOSGeometry(utm["geom"], srid=4326).wkt,resolution=10000).values("id","geom_4326").distinct("id"):
    #         if quad["id"] not in quadriculas:
    #             quadriculas.append(quad["id"])

    #### utm1x1
    # antiguas
    for utm in PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=1000).values("idquadricula__geom_4326").distinct("idquadricula"):
        for quad in Quadricula.objects.filter(geom_4326__intersects=utm["idquadricula__geom_4326"].wkt,resolution=10000).values("id","geom_4326").distinct("id"):
            if quad["id"] not in quadriculas:
                quadriculas.append(quad["id"])

    # nuevas
    for utm in CitacionsEspecie.objects.filter(idspinvasora=id, utm_1__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct("utm_1"):
        for quad in Quadricula.objects.filter(geom_4326__intersects=GEOSGeometry(utm["geom"], srid=4326).wkt,resolution=10000).values("id","geom_4326").distinct("id"):
            if quad["id"] not in quadriculas:
                quadriculas.append(quad["id"])
    # # nuevas
    # for cit in CitacionsEspecie.objects.filter(idspinvasora=id, utmx__isnull=False, utmy__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct():
    #     geom_4326 = GEOSGeometry(cit["geom"], srid=4326)
    #     geometrias.append({"geom_4326":str(geom_4326)})
    # #### utm10x10
    # # antiguas
    # for utm in PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=10000).values("idquadricula__geom_4326").distinct("idquadricula"):
    #     geometrias.append({"geom_4326":str(utm["idquadricula__geom_4326"].wkt)})
    # # nuevas
    # for utm in CitacionsEspecie.objects.filter(idspinvasora=id, utm_10__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct("utm_10"):
    #     geom_4326 = GEOSGeometry(cit["geom"], srid=4326)
    #     geometrias.append({"geom_4326":str(geom_4326)})
    # #### utm1x1
    # # antiguas
    # for utm in PresenciaSp.objects.filter(idspinvasora=id,idquadricula__resolution=1000).values("idquadricula__geom_4326").distinct("idquadricula"):
    #     geometrias.append({"geom_4326":str(utm["idquadricula__geom_4326"].wkt)})
    # # nuevas
    # for utm in CitacionsEspecie.objects.filter(idspinvasora=id, utm_1__isnull=False, geom__isnull = False, validat="SI").values("geom").distinct("utm_1"):
    #     geom_4326 = GEOSGeometry(cit["geom"], srid=4326)
    #     geometrias.append({"geom_4326":str(geom_4326)})

    resultado = json.dumps(quadriculas)
    return HttpResponse(resultado, content_type='application/json;')

#GENERAR CSV CON EL Nº DE ESPECIES Y DE CITACIONES QUE SE ENCUENTRAN EN CADA UTM10X10
def generar_csv_informe_utm10(request):

    resultado = HttpResponse(content_type='text/csv')
    resultado['Content-Disposition'] = 'attachment; filename="InformeUTM10km.csv"'

    writer = csv.writer(resultado, delimiter=str(u';').encode('utf-8'), dialect='excel', encoding='utf-8') #  quoting=csv.QUOTE_ALL,
    resultado.write(u'\ufeff'.encode('utf8')) # IMPORTANTE PARA QUE FUNCIONEN LOS ACENTOS
    writer.writerow([u'UTM 10km', u'Nº Espècies', 'Nº Citacions en punts',"Notes"])

    utms10 = Quadricula.objects.filter(resolution=10000).values("id","geom_4326").order_by("id")#id='CH14',id='EG09',id='EG02'

    # cursor = connection.cursor()
    # fetch = []
    # try:
    #     # if 'DELETE' in especies or 'delete' in especies or 'UPDATE' in especies or 'update' in especies:# toda precaucion con las querys es poca
    #     #     raise Http404('Error al generar el csv.')
    #     # especies = especies.split(",")
    #     cursor.execute('SELECT c.idspinvasora AS "IDSPINVASORA",'
    #     " (t.genere::text || ' '::text) || t.especie::text AS nom,"
    #     " t.especie,"
    #     " c.geom,"
    #     " st_transform(c.geom, 4326) AS geom_4326"
    #     " FROM citacions c,"
    #     " especieinvasora ei,"
    #     " taxon t"
    #     " WHERE ei.id::text = c.idspinvasora::text AND t.id::text = ei.idtaxon::text"
    #     " UNION ALL"
    #     ' SELECT ce.idspinvasora AS "IDSPINVASORA",'
    #     " (t.genere::text || ' '::text) || t.especie::text AS nom,"
    #     " t.especie,"
    #     " ce.geom,"
    #     " st_transform(ce.geom, 4326) AS geom_4326"
    #     " FROM citacions_especie ce,"
    #     " especieinvasora ei,"
    #     " taxon t"
    #     " WHERE ce.validat::text = 'SI'::text AND ei.id::text = ce.idspinvasora::text AND t.id::text = ei.idtaxon::text AND ce.utmx IS NOT NULL AND ce.utmy IS NOT NULL;"
    #     )
    #     #[utm["geom_4326"].wkt]) %s
    #     fetch = dictfetchall(cursor)
    #
    #     # for especie in fetch:
    #     #     ncit+=1
    #     #     #writer.writerow([especie["taxon"], especie["grup"], especie["regionativa"], especie["viesentrada"], especie["estatushistoric"], especie["estatuscatalunya"], especie["presentcatalog"],especie["presentreglamenteur"]])
    #     # return resultado
    # except:
    #     raise Http404('Error al generar el csv.')
    #
    # finally:
    #     cursor.close()
    citglobal = CitacionsGlobal.objects.all()
    for utm in utms10:
        nespecies = 0
        ncit = 0

        # Cojemos todos los tipos de utm's que esten dentro de la zona que abarca la utm(se incluira la propia utm)
        #
        # especies = PresenciaSp.objects.filter(idquadricula__in=quad).values("idspinvasora").distinct("idspinvasora")
        #
        # # para que al juntar especies y especies_2 no salga 2 veces una especie que existe en ambas ponemos el exclude
        # especies_2 = CitacionsEspecie.objects.filter(utm_10__isnull=False, utm_10__in=quad).exclude(idspinvasora__in=especies.values_list('idspinvasora',flat=True)).values("idspinvasora").distinct("idspinvasora")#"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # especies_3 = CitacionsEspecie.objects.filter(utm_1__isnull=False, utm_1__in=quad).exclude(Q(idspinvasora__in=especies.values_list('idspinvasora',flat=True)) | Q(idspinvasora__in=especies_2.values_list('idspinvasora',flat=True))).values("idspinvasora","idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie").distinct("idspinvasora")
        # # especies = PresenciaSp.objects.filter(idquadricula=utm["id"]).values("idspinvasora").distinct("idspinvasora") #,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # # para que al juntar especies y especies_2 no salga 2 veces una especie que existe en ambas ponemos el exclude
        # # especies_2 = CitacionsEspecie.objects.filter(utm_10__isnull=False, utm_10=utm["id"]).values("idspinvasora").distinct("idspinvasora")#,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # nespecies = len(list(chain(especies, especies_2, especies_3)))

        ######################
        #OJO!!!!!! que eso de que empiecen las utm1km por EG09 no significa que esten dentro de la utm10km EG09, los ids no tienen relacion entre ellos!
        #1 guaramos las utm de 1km que hay dentro de la utm10 en quad gracias al contained
        quad = Quadricula.objects.filter(geom_4326__contained=utm["geom_4326"].wkt,resolution=1000).order_by("id")#quad = Quadricula.objects.filter(id__startswith=utm["id"],resolution=1000).order_by("id")#utms de 1km dentro de la utm de 10
        #2 obtenemos las especies que hay en la utm 10 y las que han sido localizadas en utms de 1 km dentro de esa utm10
        especies = PresenciaSp.objects.filter(idquadricula=utm["id"]).values("idspinvasora").distinct("idspinvasora") #,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        especies_2 = PresenciaSp.objects.filter(idquadricula__in=quad).exclude(idspinvasora__in=especies.values_list('idspinvasora',flat=True)).values("idspinvasora").distinct("idspinvasora") #,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        #3 unimos la lista(pusimos antes los exclude para evitar que se repitan especies al unirlas)
        especies = list(chain(especies, especies_2))
        #4 Repetimos el proceso pero con las localizaciones mediante formularios
        especies_3 = CitacionsEspecie.objects.filter(utm_10__isnull=False, utm_10=utm["id"]).exclude(idspinvasora__in=especies).values("idspinvasora").distinct("idspinvasora")#,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"especies.values_list('idspinvasora',flat=True)
        especies = list(chain(especies, especies_3))
        especies_4 = CitacionsEspecie.objects.filter(utm_1__isnull=False, utm_1__in=quad).exclude(idspinvasora__in=especies).values("idspinvasora").distinct("idspinvasora")#,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        #5 una vez todas las listas estan unidas,usamos el len para obtener el nº de especies total
        especies_total=list(chain(especies, especies_4))
        nespecies = len(especies_total)

        #######################


        # especies = PresenciaSp.objects.filter(idquadricula=utm["id"]).values("idspinvasora").distinct("idspinvasora") #,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # especies_2 = PresenciaSp.objects.filter(idquadricula_in=quad).values("idspinvasora").distinct("idspinvasora") #,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # # para que al juntar especies y especies_2 no salga 2 veces una especie que existe en ambas ponemos el exclude
        # especies_3 = CitacionsEspecie.objects.filter(utm_10__isnull=False, utm_10=utm["id"]).values("idspinvasora").distinct("idspinvasora")#,"idspinvasora__idtaxon__genere","idspinvasora__idtaxon__especie"
        # nespecies = len(list(chain(especies, especies_2)))


        #cits = V_citacions_global.objects.filter(geom_4326__intersects=utm["geom_4326"].wkt).values("id")
        #6 Ahora no solo contamos la citaciones que se encuentran en la utm sino que ademas anadimos al nº de especies, las especies que se encuentren unicamente en una citacion puntual dentro de esa utm
        cits=citglobal.filter(geom_4326__intersects=utm["geom_4326"].wkt)
        ncit=cits.count()
        especies_de_citacions= cits.distinct("idspinvasora").values_list("idspinvasora",flat=True)
        nespecies_de_citacions= Especieinvasora.objects.filter(id__in=especies_de_citacions).exclude(id__in=especies_total).count()
        nespecies+=nespecies_de_citacions
        #ncit = len(list(cits))
        #resultado.append({"utm":utm["idquadricula"],"nespecies":nespecies,"ncit":ncit})
        #una pequeña comprovacion para ver que no haya duplicidad
        for sp in especies_de_citacions:
            if sp in especies_total:
                writer.writerow("#Error")
        #7 Finalmente anadimos el resultado,pero si se cumple el punto 6 y hay especies solo en citaciones,lo comunicaremos con una nota en el csv
        if nespecies_de_citacions>0:
            mensaje=u"*De les "+str(nespecies)+u" espècies,n'hi han "+str(nespecies_de_citacions)+u" localitzades únicament en punts dins de la utm."
            writer.writerow([utm["id"], nespecies, ncit,mensaje])
        else:
            writer.writerow([utm["id"],nespecies,ncit,""])

        # #codigo de testeo:
        # if(utm["id"]=='EH00'):
        #     ncit=0
    #especies y citaciones sin asignar en alguna utm
    # nespecies_noassign=citglobal.exclude(idspinvasora__in=PresenciaSp.objects.all().values_list('idspinvasora',flat=True)).count()
    #
    # writer.writerow("","","","*Nota: Hi ha especies",nespecies_noassign)
    # #
    return resultado
    #resultado_final = json.dumps(resultado)
    # return HttpResponse(resultado_final, content_type='application/json;')

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
# @login_required(login_url='/login/')
def view_formularis_localitats_especie(request):
    id_imatge_principal=""
    ids_imatges = ""
    if "ids_imatges" in request.POST:
        ids_imatges = request.POST["ids_imatges"]
    imatges=[]
    id_form=""
    if request.user.is_authenticated():
        usuari = request.user.username
    else:
        usuari = u"Anònim"
    nuevo="1"
    admin=False
    if request.method == 'POST':
        if request.user.groups.filter(name="Admins"):
            admin=True

        try:
            id_form=request.POST["id_form"]
            instance = get_object_or_404(CitacionsEspecie, id=id_form)
            # form = CitacionsEspeciesForm(instance=instance)
        except:
            instance = None
            #nuevo = "1"
            #form = CitacionsEspeciesForm

        try:
            id_imatge_principal = ImatgesCitacions.objects.get(id_citacio_especie=request.POST["id_form"],tipus="principal").id
            for img in ImatgesCitacions.objects.filter(id_citacio_especie=request.POST["id_form"],tipus="secundaria").values("id"):
                ids_imatges=ids_imatges+str(img["id"])+","
        except:
            None

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
            camps_obligatoris = ['idspinvasora','data','contacte'] # 'NIP'
            formulario_clean  = form.cleaned_data

            if formulario_clean["idspinvasora"] == "00000":
                camps_obligatoris.append("especie")

            # Segun el tipo de corrdenadas que nos de el usuario,haremos obligatorios ciertos inputs
            if request.POST["tipus_coordenades"] == "1":
                camps_obligatoris.append("utmx")
                camps_obligatoris.append("utmy")
                # camps_obligatoris.append("utmz")
            else:
                if request.POST["tipus_coordenades"] == "2":
                    camps_obligatoris.append("utm_10")
                else:
                    if request.POST["tipus_coordenades"] == "3":
                        camps_obligatoris.append("utm_1")
            #
            # Verificamos que el usuario haya dado la imagen principal por lo menos
            if request.POST["id_imatge_principal"] != "":
                id_imatge_principal = request.POST["id_imatge_principal"]
            else:
                form.add_error(None,"No has penjat la foto identificativa.")


            # Ahora verificamos que no haya subido secundarias de mas
            if ids_imatges != "":
                ids_imatges = request.POST["ids_imatges"]
                imatges = request.POST["ids_imatges"].split(",")
                # el ultimo tiene un elemento vacio ya que se pasa una coma suelta
                del imatges[-1]
                if len(imatges) > 6:
                    errorcount = "No pots pujar mes de 6 imatges opcionals." #Faltan "+str(7-len(imatges))+" imatges.
                    form.add_error(None,errorcount)
            # else:
            #     form.add_error(None,"No has penjat cap imatge.")

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
                        if request.POST["formulari_validat"] == "SI":
                            form.validat = "SI"
                        else:
                            form.validat = "NO"
                    else:
                        form.validat = "NO"

                form.usuari=usuari
                #
                if nuevo=="1":
                    form.data_creacio=datetime.date.today().strftime('%d-%m-%Y')
                form.data_modificacio=datetime.date.today().strftime('%d-%m-%Y')
                #
                try:
                    if request.POST["tipus_coordenades"] == "1":
                        punto = GEOSGeometry('POINT(' + request.POST["utmx"] + ' ' + request.POST["utmy"] + ')',srid=23031)
                        form.geom = punto
                        # punto2 = punto.transform(4326,clone=True)
                        # form.geom_4326 = punto2
                        # punto2 = GEOSGeometry(punto, srid=4326)
                    # punto = 1
                except:
                    None
                new_form = form.save()
                try:
                    img_principal = ImatgesCitacions.objects.get(id=id_imatge_principal)
                    if nuevo=="0":#Si no es nuevo hay que substituir la imagen(moviandola antes a temp)
                        # si al editar el proyecto se ha modificado la imagen principal:
                        if img_principal.fitxer.name != ImatgesCitacions.objects.get(id_citacio_especie=id_form,tipus="principal").fitxer.name:
                            img_borrar = ImatgesCitacions.objects.get(id_citacio_especie=id_form, tipus="principal")
                            #img_borrar.cambiar_localizacion(1)
                            #img_borrar.save()
                            ##### mover de imatges citacions especies al temp
                            img_borrar.temporal = True
                            initial_path = img_borrar.fitxer.path
                            img_borrar.fitxer.name = img_borrar.fitxer.name.replace('imatges_citacions_especies/', '')
                            img_borrar.fitxer.name = 'imatges_temp/' + img_borrar.fitxer.name
                            new_path = settings.MEDIA_ROOT  + '/' + img_borrar.fitxer.name
                            os.rename(initial_path, new_path)
                            #####
                            img_borrar.delete()
                            # ImatgesCitacions.objects.get(id_citacio_especie=id_form, tipus="principal").delete()

                            #####este parrafo ha de ser igual que el siguient
                            img_principal.id_citacio_especie = CitacionsEspecie.objects.get(id=form.id)
                            img_principal.temporal = False
                            ##### mover de temp al imatges citacions especies
                            initial_path = img_principal.fitxer.path
                            img_principal.fitxer.name = img_principal.fitxer.name.replace('imatges_temp/', '')
                            img_principal.fitxer.name = 'imatges_citacions_especies/' + img_principal.fitxer.name
                            new_path = settings.MEDIA_ROOT + '/' + img_principal.fitxer.name
                            os.rename(initial_path, new_path)
                            #####
                            img_principal.save()  # guardar(2)
                    else:
                        img_principal.id_citacio_especie = CitacionsEspecie.objects.get(id=form.id)
                        img_principal.temporal = False
                        ##### mover de temp al imatges citacions especies
                        initial_path = img_principal.fitxer.path
                        img_principal.fitxer.name = img_principal.fitxer.name.replace('imatges_temp/', '')
                        img_principal.fitxer.name = 'imatges_citacions_especies/' + img_principal.fitxer.name
                        new_path = settings.MEDIA_ROOT + '/' + img_principal.fitxer.name
                        os.rename(initial_path, new_path)
                        #####
                        img_principal.save()  # guardar(2)
                except:
                    return HttpResponseRedirect('/formularis/')

                if len(imatges)>0:
                    for imatge in imatges:
                        if imatge != "":
                            img = ImatgesCitacions.objects.get(id=imatge)
                            img.id_citacio_especie = CitacionsEspecie.objects.get(id=form.id)
                            img.temporal = False
                            ##### mover de temp al imatges citacions especies
                            initial_path = img.fitxer.path
                            img.fitxer.name = img.fitxer.name.replace('imatges_temp/', '')
                            img.fitxer.name = 'imatges_citacions_especies/' + img.fitxer.name
                            new_path = settings.MEDIA_ROOT  + '/' + img.fitxer.name
                            os.rename(initial_path, new_path)
                            #####
                            img.save()
                # nuevo="0"
                if request.user.is_authenticated():
                    return HttpResponseRedirect('/formularis/')
                else:
                    return HttpResponseRedirect('/base_dades/')




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
    context={'form':form,'especies':especies,'id_imatge_principal':id_imatge_principal,'ids_imatges':ids_imatges,'nuevo':nuevo,'id_form':id_form}
    return render(request,'exocat/formularis_localitats_especie.html',context)

# Formulario de ACA para las citacions !no utilizable de momento
# @login_required(login_url='/login/')
# def view_formularis_aca(request):
#     if request.method == 'POST':
#         form = CitacionsACAForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#     else:
#         form = CitacionsACAForm()
#     context={'form':form}
#     return render(request,'exocat/formularis_aca.html',context)

# @login_required(login_url='/login/')
def view_upload_imatge_citacions_especie(request):

    if request.GET:
    # def get(self, request):
        resultado = []
        if request.GET.get("id_imatge_principal") is not None: # si es la principal
            img = ImatgesCitacions.objects.get(id=request.GET["id_imatge_principal"])
            resultado={'name': img.fitxer.name, 'url': img.fitxer.url, 'id': img.id}

        else:
            imatges = request.GET["ids_imatges"].split(",")
            for imatge in imatges:
                if imatge != "":
                    img = ImatgesCitacions.objects.get(id=imatge)
                    resultado.append({'name': img.fitxer.name, 'url': img.fitxer.url, 'id': img.id})


        return JsonResponse(resultado,safe=False)
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
        max_file_size = 10485760

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
                    # form.cleaned_data["temporal"] = True
                    form = form.save(commit=False)  # Ojo esto es importante para modificar los campos del forma antes de guardar
                    form.temporal=True
                    # form.cambiar_localizacion(1)
                    imatge = form.save()
                    data = {'is_valid':True, 'name': form.fitxer.name , 'url': form.fitxer.url, 'id':form.id }
        else:
            data = {"is_valid":False, 'errormessage':'Error al pujar la imatge.'}
        return JsonResponse(data)

@login_required(login_url='/login/')
def view_delete_imatge_citacions_especie(request):
    try:
        instancia = ImatgesCitacions.objects.get(id=request.POST["id"])
        ##### mover de imatges citacions especies al temp OJO que este es diferente a los demas en el initial path
        initial_path = instancia.fitxer.path
        instancia.fitxer.name = instancia.fitxer.name.replace('imatges_citacions_especies/', '')
        instancia.fitxer.name = instancia.fitxer.name.replace('imatges_temp/', '')
        instancia.fitxer.name = 'imatges_temp/' + instancia.fitxer.name
        new_path = settings.MEDIA_ROOT  + '/' + instancia.fitxer.name
        os.rename(initial_path, new_path)
        #####
        instancia.delete()
        data = {'is_valid': True}
        return JsonResponse(data)
    except:
        return None

@login_required(login_url='/login/')
def json_taula_formularis_usuari(request):
    formularios=[]
    nom_especie = ""
    if request.user.is_authenticated():
        formscitacions=[]
        if request.user.groups.filter(name="Admins"):
            formscitacions=CitacionsEspecie.objects.all().values("id","especie","idspinvasora","usuari","validat","data_creacio","data_modificacio","contacte","NIP")
        else:
            formscitacions = CitacionsEspecie.objects.filter(usuari=request.user.username).values("id","especie","idspinvasora","usuari","validat","data_creacio","data_modificacio","contacte","NIP")

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

            usuari = form["usuari"]
            try:
                if form["contacte"] != "" and usuari=="Anònim" and form["contacte"] is not None:
                    usuari = usuari +u" ( "+form["contacte"]
                    if form["NIP"] != "" and form["NIP"] is not None:
                        usuari = usuari + u" - codi:"+form["NIP"]
                    usuari = usuari +u" )"
            except:
                usuari = usuari
            formularios.append({"id":form["id"],"especie":nom_especie,"usuari":usuari,"validat":form["validat"],"data_creacio":form["data_creacio"],"data_modificacio":form["data_modificacio"]})

    resultado = json.dumps(formularios)
    return HttpResponse(resultado, content_type='application/json;')

# CITACIONES DE EXOAQUA POR REVISAR
@login_required(login_url='/login/')
def view_revisar_citacions_aca(request):
    especies_autocomplete = []
    for especie in Especieinvasora.objects.all().values("id","idtaxon__genere","idtaxon__especie","idtaxon__subespecie").order_by("idtaxon__genere"):
        # nombre de la especie(se juntan el genere con especie y subespecie)
        id = especie["id"]
        genere = especie["idtaxon__genere"]
        especiestr = especie["idtaxon__especie"]
        subespeciestr = especie["idtaxon__subespecie"]
        if especiestr is not None:
            genere = genere + " " + especiestr
        if subespeciestr is not None:
            genere = genere + u" [Subespècie: " + subespeciestr + " ]"
        especies_autocomplete.append({"id":id,"especie":genere})

    context = {'especies_autocomplete':especies_autocomplete,'titulo': "REVISAR CITACIONS EXOAQUA", 'usuari': request.user.username}
    return render(request, 'exocat/revisar_citacions_aca.html', context)

# VIEW PARA INTRODUCIR CITACIONES MEDIANTE FICHEROS
@login_required(login_url='/login/')
def view_introduccio_citacions_fitxer(request):
    context = {'titulo': "INTRODUIR CITACIONS FITXER", 'usuari': request.user.username}
    return render(request, 'exocat/introduccio_citacions_fitxer.html', context)


# AJAX DE LES CITACIONS DE EXOAQUA PER REVISAR
@login_required(login_url='/login/')
def json_taula_revisar_citacions_aca(request):
    especies = []
    for especie in TaxonExoaquaRevisar.objects.all():
        especies.append({'id':especie.id,'id_especie_exoaqua':especie.id_especie_exoaqua,'nom':especie.nom_especie,'data':'{:%d-%m-%Y}'.format(especie.data.date()),'revisat':especie.revisat})

    resultado = json.dumps(especies)
    return HttpResponse(resultado, content_type='application/json;')

# AJAX PER REVISAR UNA ESPECIE DE EXOAQUA I ASSIGNARLE UN ID DE EXOCAT
@login_required(login_url='/login/')
def post_revisar_citacions_aca(request):
    try:
        if request.user.groups.filter(name="Admins"):
            if Especieinvasora.objects.filter(id=request.POST["id_especie_exocat"]).exists():
                if TaxonExoaquaRevisar.objects.filter(id=request.POST['id'],revisat=0).exists():
                    taxonarevisar = TaxonExoaquaRevisar.objects.get(id=request.POST['id'])
                    id_especie_exoaqua = taxonarevisar.id_especie_exoaqua
                    r = requests.post('http://delfos.creaf.uab.es/exoaqua_test/exoaqua/api/validataxon.htm',{'id':id_especie_exoaqua,'idexo':request.POST['id_especie_exocat']})
                    if r.status_code == 200:
                        taxonarevisar.id_especie_exocat = request.POST["id_especie_exocat"]
                        taxonarevisar.revisat = 1
                        taxonarevisar.save()
                        return HttpResponse("{}", content_type='application/json;')
                    else:
                        response = JsonResponse({"error": "Error al guardar l'espécie. Torna-ho a provar en uns minuts o contacta amb l'administrador."})
                        response.status_code = 400
                        return response
            else:
                response = JsonResponse({"error": "Error: El nom de l'espécie no es correcte o aquesta no existeix a la base de dades d'Exocat."})
                response.status_code = 400
                return response
        else:

            response = JsonResponse({"error": "Error"})
            response.status_code = 400
            return response
    except:
        response = JsonResponse({"error": "Error"})
        response.status_code = 400
        return response
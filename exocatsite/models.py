# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
#from django.db import models
import migrations

class Actuacio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey('Especieinvasora', models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    iddoc = models.ForeignKey('Documents', models.DO_NOTHING, db_column='iddoc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actuacio'

class Extensions(models.Model):
    idextensio = models.CharField(primary_key=True, max_length=100)
    extensio = models.CharField(max_length=25, blank=True, null=True)
    descripcio = models.CharField(max_length=500, blank=True, null=True)
    fitxericona = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extensions'

# class Imatges(models.Model): # Ojo que este en realidad se relaciona con la especie a traves del model "Imatge"
#     idimatge = models.CharField(primary_key=True, max_length=100)
#     titol = models.CharField(max_length=4000, blank=True, null=True)
#     observacions = models.CharField(max_length=500, blank=True, null=True)
#     nomoriginal = models.CharField(max_length=255, blank=True, null=True)
#     thumbnail = models.BinaryField(blank=True, null=True)
#     fitxer = models.BinaryField(blank=True, null=True)
#     visualitzable = models.CharField(max_length=1, blank=True, null=True)
#     tag = models.CharField(max_length=255, blank=True, null=True)
#
#     #FOREIGN KEYS
#     idextensio = models.ForeignKey(Extensions, models.DO_NOTHING,related_name="id_imatge_extensio", db_column='idextensio', blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'imatges'

class Citacions(models.Model):
    especie = models.CharField(max_length=255, blank=True, null=True)
    idspinvasora = models.CharField(max_length=100, blank=True, null=True)
    grup = models.CharField(max_length=255, blank=True, null=True)
    utmx = models.FloatField(blank=True, null=True)
    utmy = models.FloatField(blank=True, null=True)
    localitat = models.CharField(max_length=255, blank=True, null=True)
    municipi = models.CharField(max_length=255, blank=True, null=True)
    comarca = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    data = models.CharField(max_length=100, blank=True, null=True)
    autor_s = models.CharField(max_length=255, blank=True, null=True)
    citacio = models.CharField(max_length=255, blank=True, null=True)
    font = models.CharField(max_length=255, blank=True, null=True)
    referencia = models.CharField(max_length=255, blank=True, null=True)
    observacions = models.CharField(max_length=4000, blank=True, null=True)
    tipus_cita = models.CharField(max_length=100, blank=True, null=True)
    habitat = models.CharField(max_length=100, blank=True, null=True)
    tipus_mort = models.CharField(max_length=100, blank=True, null=True)
    abundancia = models.CharField(max_length=100, blank=True, null=True)
    codi_aca = models.CharField(max_length=100, blank=True, null=True)
    codi_estacio = models.CharField(max_length=100, blank=True, null=True)
    ind_ha = models.FloatField(blank=True, null=True)
    ind_capt = models.IntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    geom_4326 = models.GeometryField()  # modificado

    class Meta:
        managed = False
        db_table = 'citacions'

class Comarques(models.Model):
    gid = models.AutoField(primary_key=True)
    codicomar = models.CharField(max_length=254, blank=True, null=True)
    nomcomar = models.CharField(max_length=254, blank=True, null=True)
    areacomar = models.FloatField(blank=True, null=True)
    dataalta = models.CharField(max_length=200, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'comarques_4326'

class ConquesPrincipals(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    codi_aca = models.CharField(max_length=254, blank=True, null=True)
    nom_conca = models.CharField(max_length=254, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'conques_principals'

class Document(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey('Especieinvasora', models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    iddoc = models.ForeignKey('Documents', models.DO_NOTHING, db_column='iddoc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document'


class Documents(models.Model):
    iddocument = models.CharField(primary_key=True, max_length=100)
    titol = models.CharField(max_length=500, blank=True, null=True)
    observacions = models.CharField(max_length=500, blank=True, null=True)
    idextensio = models.ForeignKey('Extensions', models.DO_NOTHING, db_column='idextensio', blank=True, null=True)
    nomoriginal = models.CharField(max_length=255, blank=True, null=True)
    fitxer = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documents'

class Especieinvasora(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    observacions = models.CharField(max_length=4000, blank=True, null=True)
    present_catalogo = models.CharField(max_length=1, blank=True, null=True)
    reglament_ue = models.CharField(max_length=1, blank=True, null=True) # anadido en la bdd el 29-05-1028
    regio_nativa = models.CharField(max_length=1000, blank=True, null=True) # modificado

    # FOREIGN KEYS *Ojo importante el related name!

    idtaxon = models.ForeignKey('Taxon', models.DO_NOTHING,related_name='id_taxon', db_column='idtaxon', blank=True, null=True)
    idestatushistoric = models.ForeignKey('Estatus', models.DO_NOTHING,related_name='estatushistoric', db_column='idestatushistoric', blank=True, null=True) # modificado
    idestatuscatalunya = models.ForeignKey('Estatus', models.DO_NOTHING,related_name='estatus_atalunya', db_column='idestatuscatalunya', blank=True, null=True)# modificado
    idimatgeprincipal = models.ForeignKey('Imatges', models.DO_NOTHING,related_name='id_imatge_principal', db_column='idimatgeprincipal', blank=True, null=True)
    idestatusgeneral = models.ForeignKey('Estatus', models.DO_NOTHING,related_name='estatusgeneral', db_column='idestatusgeneral', blank=True, null=True)# modificado

    class Meta:
        managed = False
        db_table = 'especieinvasora'

# class Imatge(models.Model): #
#     id = models.CharField(primary_key=True, max_length=100)
#     tag = models.CharField(max_length=255, blank=True, null=True)
#
#     #FOREIGN KEYS
#     idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING,related_name="id_especie_imatge", db_column='idespecieinvasora', blank=True, null=True)
#     idimatge = models.ForeignKey('Imatges', models.DO_NOTHING,related_name="id_imatge_imatge", db_column='idimatge', blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'imatge'

class Estatus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100, blank=True, null=True)
    estatus_catalunya = models.BooleanField()
    estatus_historic = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'estatus'

class Habitat(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    habitat = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habitat'


class Habitatespecie(models.Model):
    idspinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING,related_name='id_especie_habitat', db_column='idspinvasora', blank=True, null=True)
    idhabitat = models.ForeignKey(Habitat, models.DO_NOTHING,related_name='id_habitat', db_column='idhabitat', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habitatespecie'

class ExoaquaToExocat(models.Model):
    id_exoaqua = models.CharField(max_length=100, blank=True, null=True)
    id_exocat = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exoaqua_to_exocat'

class Grup(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grup'

class Grupespecie(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    #FOREIGN KEYS
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING,related_name='id_especie_grup', db_column='idespecieinvasora', unique=True, blank=True, null=True)
    idgrup = models.ForeignKey(Grup, models.DO_NOTHING,related_name='id_grup', db_column='idgrup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupespecie'

class Viaentrada(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    viaentrada = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viaentrada'

class Viaentradaespecie(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    #FOREIGN KEYS
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING,related_name='id_especie_viaentrada', db_column='idespecieinvasora', blank=True, null=True)
    idviaentrada = models.ForeignKey(Viaentrada, models.DO_NOTHING,related_name='id_viaentrada', db_column='idviaentrada', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viaentradaespecie'

class MassaAiguaTaxon(models.Model):
    id_taxon_exoaqua = models.CharField(max_length=100, blank=True, null=True)
    id_localitzacio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'massa_aigua_taxon'


class MassesAigua(models.Model):
    gid = models.AutoField(primary_key=True)
    id = models.CharField(max_length=100, blank=True, null=True)
    codi_aca = models.CharField(max_length=100, blank=True, null=True)
    tipus_geom = models.CharField(max_length=1, blank=True, null=True)
    nom = models.CharField(max_length=254, blank=True, null=True)
    idconca = models.CharField(max_length=100, blank=True, null=True)
    idcategor = models.CharField(max_length=100, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'masses_aigua'

class ActualitzacioDades08072015(models.Model):
    id = models.AutoField(primary_key=True)
    codi_aca = models.CharField(max_length=200, blank=True, null=True)
    utmx_etrs89 = models.CharField(max_length=200, blank=True, null=True)
    utmy_etrs89 = models.CharField(max_length=200, blank=True, null=True)
    localitzacio = models.CharField(max_length=200, blank=True, null=True)
    codi_sp = models.CharField(max_length=200, blank=True, null=True)
    data_cita = models.CharField(max_length=200, blank=True, null=True)
    autor_cita = models.CharField(max_length=200, blank=True, null=True)
    font_cita = models.CharField(max_length=200, blank=True, null=True)
    observacions = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actualitzacio_dades_08_07_2015'

    def codi_nom(self):
        if MassesAigua.objects.filter(codi_aca=self.codi_aca):
            return "{0} - {1}".format(self.codi_aca,MassesAigua.objects.filter(codi_aca=self.codi_aca).first().only("codi_aca"))
        else:
            return self.codi_aca


class Nomvulgar(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nomvulgar = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'nomvulgar'


class Nomvulgartaxon(models.Model):
    id = models.CharField(primary_key=True, max_length=100)


    #FOREIGN KEYS
    idtaxon = models.ForeignKey('Taxon', models.DO_NOTHING,related_name='id_respecietaxon', db_column='idtaxon')
    idnomvulgar = models.ForeignKey(Nomvulgar, models.DO_NOTHING,related_name='id_nomvulgar', db_column='idnomvulgar')
    idnomvulgar_eng = models.ForeignKey(Nomvulgar, models.DO_NOTHING,related_name='id_nomvulgareng', db_column='idnomvulgar_eng', blank=True, null=True)
    idnomvulgar_es = models.ForeignKey(Nomvulgar, models.DO_NOTHING,related_name='id_nomvulgares', db_column='idnomvulgar_es', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nomvulgartaxon'

class Regionativa(models.Model):
    id = models.CharField(primary_key=True, max_length=100)

    #FOREIGN KEYS
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING,related_name='id_especie_regio', db_column='idespecieinvasora', blank=True, null=True)
    idzonageografica = models.ForeignKey('Zonageografica', models.DO_NOTHING,related_name='id_zonageografica', db_column='idzonageografica', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regionativa'

class PresenciaSp(models.Model):
    idquadricula = models.ForeignKey('Quadricula', models.DO_NOTHING, db_column='idquadricula', blank=True, null=True)
    idspinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idspinvasora', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'presencia_sp'


class QuadTemp(models.Model):
    gid = models.AutoField(primary_key=True)
    precision_field = models.DecimalField(db_column='precision_', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it ended with '_'.
    resolution = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    code_utm_1 = models.CharField(max_length=254, blank=True, null=True)
    field_xmin = models.DecimalField(db_column='__xmin', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    field_xmax = models.DecimalField(db_column='__xmax', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row. Field renamed because it started with '_'.
    ymin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    ymax = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    id_show = models.CharField(max_length=254, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'quad_temp'


class Quadricula(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    precision_m = models.FloatField(blank=True, null=True)
    resolution = models.FloatField(blank=True, null=True)
    code_utm_10 = models.CharField(max_length=4, blank=True, null=True)
    field_xmin = models.FloatField(db_column='_xmin', blank=True, null=True)  # Field renamed because it started with '_'.
    field_xmax = models.FloatField(db_column='_xmax', blank=True, null=True)  # Field renamed because it started with '_'.
    field_ymin = models.FloatField(db_column='_ymin', blank=True, null=True)  # Field renamed because it started with '_'.
    field_ymax = models.FloatField(db_column='_ymax', blank=True, null=True)  # Field renamed because it started with '_'.
    #quadre = models.TextField(blank=True, null=True)  # This field type is a guess.
    quadre = models.GeometryField()
    geom_4326 = models.GeometryField() # modificado

    class Meta:
        managed = False
        db_table = 'quadricula'

class Taxon(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nomsp = models.CharField(max_length=100, blank=True, null=True)
    tesaurebiocat = models.CharField(max_length=100, blank=True, null=True)
    codibiocat = models.CharField(max_length=100, blank=True, null=True)
    genere = models.CharField(max_length=100, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)
    autorespecie = models.CharField(max_length=100, blank=True, null=True)
    subespecie = models.CharField(max_length=100, blank=True, null=True)
    autorsubespecie = models.CharField(max_length=100, blank=True, null=True)
    varietat = models.CharField(max_length=100, blank=True, null=True)
    autorvarietat = models.CharField(max_length=100, blank=True, null=True)
    subvarietat = models.CharField(max_length=100, blank=True, null=True)
    autorsubvarietat = models.CharField(max_length=100, blank=True, null=True)
    forma = models.CharField(max_length=100, blank=True, null=True)
    autorforma = models.CharField(max_length=100, blank=True, null=True)
    codieorca = models.CharField(max_length=100, blank=True, null=True)
    familia = models.CharField(max_length=100, blank=True, null=True)
    taxonomicelements_id = models.CharField(max_length=100, blank=True, null=True)
    scientificname = models.CharField(max_length=100, blank=True, null=True)
    highertaxon = models.CharField(max_length=100, blank=True, null=True)
    kingdom = models.CharField(max_length=100, blank=True, null=True)
    phylum = models.CharField(max_length=100, blank=True, null=True)
    taxonomicelement_class = models.CharField(max_length=100, blank=True, null=True)
    taxonomicelement_order = models.CharField(max_length=100, blank=True, null=True)
    family = models.CharField(max_length=100, blank=True, null=True)
    genus = models.CharField(max_length=100, blank=True, null=True)
    specificepithet = models.CharField(max_length=100, blank=True, null=True)
    infraspecificrank = models.CharField(max_length=100, blank=True, null=True)
    infraspecificepithet = models.CharField(max_length=100, blank=True, null=True)
    authoryearofscientificname = models.CharField(max_length=100, blank=True, null=True)
    nomenclaturalcode = models.CharField(max_length=100, blank=True, null=True)
    c_esp = models.CharField(max_length=100, blank=True, null=True)
    c_e_o = models.CharField(max_length=100, blank=True, null=True)
    c_pcsb = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxon'

class Zonageografica(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'zonageografica'

class Imatges(models.Model):
    idimatge = models.CharField(primary_key=True, max_length=100)
    titol = models.CharField(max_length=4000, blank=True, null=True)
    observacions = models.CharField(max_length=500, blank=True, null=True)
    nomoriginal = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.BinaryField(blank=True, null=True)
    fitxer = models.BinaryField(blank=True, null=True)
    fitxer = models.FileField(upload_to='imatges_especies', blank=True, null=True)
    visualitzable = models.CharField(max_length=1, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    # FOREIGN KEYS
    idextensio = models.ForeignKey(Extensions, models.DO_NOTHING, db_column='idextensio', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imatges'

class Imatge(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    tag = models.CharField(max_length=255, blank=True, null=True)

    # FOREIGN KEYS
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idespecieinvasora',
                                          blank=True, null=True)
    idimatge = models.ForeignKey('Imatges', models.DO_NOTHING, db_column='idimatge', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imatge'

# ------------------------------------------------- MODIFICADO


class CitacionsEspecie(models.Model):
    id = models.AutoField(primary_key=True)
    especie = models.CharField(max_length=255, blank=True, null=True)
    # idspinvasora = models.ForeignKey(Especieinvasora, null=True) # FOREIGN
    idspinvasora = models.CharField(max_length=255, blank=True, null=True)
    data = models.CharField(max_length=100, blank=True, null=True)

    comarca = models.CharField(max_length=100, blank=True, null=True)
    municipi = models.CharField(max_length=255, blank=True, null=True)
    localitat = models.CharField(max_length=255, blank=True, null=True)
    finca = models.CharField(max_length=255, blank=True, null=True)
    paratge = models.CharField(max_length=255, blank=True, null=True)
    utmx = models.FloatField(blank=True, null=True)
    utmy = models.FloatField(blank=True, null=True)
    utmz = models.FloatField(blank=True, null=True)
    utm_10 = models.CharField(max_length=4, blank=True, null=True)
    utm_1 = models.CharField(max_length=6, blank=True, null=True)

    propietari_nom = models.CharField(max_length=255, blank=True, null=True)
    adreca = models.CharField(max_length=255, blank=True, null=True)
    poblacio = models.CharField(max_length=255, blank=True, null=True)
    telefon = models.CharField(max_length=255, blank=True, null=True)

    qual_terreny = models.CharField(max_length=255, blank=True, null=True)

    espai_natural_protegit = models.CharField(max_length=255, blank=True, null=True)
    espai_nom = models.CharField(max_length=255, blank=True, null=True)

    superficie_ocupada = models.CharField(max_length=100, blank=True, null=True)

    presencia = models.CharField(max_length=255, blank=True, null=True)

    estat_invasio = models.CharField(max_length=255, blank=True, null=True) # foreign de estatus?

    observacions = models.CharField(max_length=4000, blank=True, null=True)

    grup = models.CharField(max_length=255, blank=True, null=True)

    # imatges = models.FileField(upload_to='imatges',blank=True,null=True)

    # imatge_panoramica = models.ForeignKey('Imatges', models.DO_NOTHING, related_name='citacio_imatge_panoramica', blank=True, null=True)
    # imatge_detall_espcie = models.ForeignKey('Imatges', models.DO_NOTHING, related_name='citacio_imatge_detall_especie', blank=True, null=True)
    # imatge_detall_localitat_1 = models.ForeignKey('Imatges', models.DO_NOTHING, related_name='citacio_imatge_detall_localitat_1',blank=True, null=True)
    # imatge_detall_localitat_2 = models.ForeignKey('Imatges', models.DO_NOTHING,related_name='citacio_imatge_detall_localitat_2', blank=True,null=True)

    contacte = models.EmailField(blank=True,null=True)
    NIP = models.CharField(max_length=255, blank=True, null=True)
    validat = models.CharField(max_length=255, blank=True, null=True)

    usuari = models.CharField(max_length=255, blank=True, null=True)  # usuario que ha creado el formulario
    data_creacio = models.CharField(max_length=100, blank=True, null=True)
    data_modificacio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'citacions_especie'

#######
# localizacion =  'imatges_temp/'
#
# def cambiar_localizacion(tipo):
#     if tipo == 1:
#         setattr(models, localizacion, str('imatges_temp/'))
#     else:
#         if tipo == 2:
#             localizacion = 'imatges_citacions_especies/'
#
# def get_image_path(instance, filename):
#     # if instance.temporal==True:
#     #     return localizacion+'{0}'.format(filename)
#     # else:
#     return localizacion+'{0}'.format(filename)
def upload_path_handler(instance, filename):
    if instance.temporal==True:
        return 'imatges_temp/{0}'.format(filename)
    else:
        return 'imatges_citacions_especies/{0}'.format(filename)


class ImatgesCitacions(models.Model):
    fitxer = models.FileField(upload_to=upload_path_handler,blank=True,null=True)
    id_citacio_especie = models.ForeignKey(CitacionsEspecie, related_name='imatges_citacio_especie', blank=True, null=True)
    tipus = models.CharField(max_length=255, blank=True, null=True)
    data_pujada = models.DateTimeField(auto_now_add=True)
    temporal = models.BooleanField()
    class Meta:
        managed = True
        db_table = 'imatges_citacions_especie'

    def guardar(self,tipo):
        if tipo == 1:# imagen temporal
            self.fitxer.file.upload_to='imatges_temp'
            self.save()
        else:
            if tipo == 2:
                self.fitxer.file.upload_to ='imatges_citacions_especies'
                self.save()
class CitacionsACA(models.Model):
    id = models.AutoField(primary_key=True)
    nom_especie = models.CharField(max_length=255, blank=True, null=True)
    codi_ma = models.CharField(max_length=255, blank=True, null=True)
    codi_especie = models.CharField(max_length=255, blank=True, null=True)
    data_cita = models.CharField(max_length=255, blank=True, null=True)
    nom_ma = models.CharField(max_length=255, blank=True, null=True)
    grup = models.CharField(max_length=255, blank=True, null=True)
    categoria_aca = models.CharField(max_length=255, blank=True, null=True)
    utm_x = models.FloatField(blank=True, null=True)
    utm_y = models.FloatField(blank=True, null=True)
    localitzacio = models.CharField(max_length=500, blank=True, null=True)
    autor_cita = models.CharField(max_length=255, blank=True, null=True)
    font_cita = models.CharField(max_length=255, blank=True, null=True)
    observacions = models.CharField(max_length=500, blank=True, null=True)
    data = models.CharField(max_length=100, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'citacions_ACA'
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Actuacio(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey('Especieinvasora', models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    iddoc = models.ForeignKey('Documents', models.DO_NOTHING, db_column='iddoc', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actuacio'


class ActualitzacioDades08072015(models.Model):
    id = models.CharField(max_length=200, blank=True, null=True)
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BioUtmGrid(models.Model):
    id = models.CharField(max_length=6, blank=True, null=True)
    utm_x_c = models.FloatField(blank=True, null=True)
    utm_y_c = models.FloatField(blank=True, null=True)
    precision_m = models.FloatField(blank=True, null=True)
    resolution = models.FloatField(blank=True, null=True)
    code_x_y = models.CharField(max_length=13, blank=True, null=True)
    code_utm = models.CharField(max_length=6, blank=True, null=True)
    code_utm_100 = models.CharField(max_length=2, blank=True, null=True)
    code_utm_10 = models.CharField(max_length=4, blank=True, null=True)
    code_utm_1 = models.CharField(max_length=6, blank=True, null=True)
    wgs84_x_c = models.FloatField(blank=True, null=True)
    wgs84_y_c = models.FloatField(blank=True, null=True)
    area_cat = models.FloatField(blank=True, null=True)
    perimetre_cat = models.FloatField(blank=True, null=True)
    coast = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bio_utm_grid'


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    idtaxon = models.ForeignKey('Taxon', models.DO_NOTHING, db_column='idtaxon', blank=True, null=True)
    idestatushistoric = models.ForeignKey('Estatus', models.DO_NOTHING, db_column='idestatushistoric', blank=True, null=True)
    idestatuscatalunya = models.ForeignKey('Estatus', models.DO_NOTHING, db_column='idestatuscatalunya', blank=True, null=True)
    idimatgeprincipal = models.ForeignKey('Imatges', models.DO_NOTHING, db_column='idimatgeprincipal', blank=True, null=True)
    observacions = models.CharField(max_length=4000, blank=True, null=True)
    present_catalogo = models.CharField(max_length=1, blank=True, null=True)
    idestatusgeneral = models.ForeignKey('Estatus', models.DO_NOTHING, db_column='idestatusgeneral', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'especieinvasora'


class Estatus(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estatus'


class ExoaquaToExocat(models.Model):
    id_exoaqua = models.CharField(max_length=100, blank=True, null=True)
    id_exocat = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exoaqua_to_exocat'


class Extensions(models.Model):
    idextensio = models.CharField(primary_key=True, max_length=100)
    extensio = models.CharField(max_length=25, blank=True, null=True)
    descripcio = models.CharField(max_length=500, blank=True, null=True)
    fitxericona = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'extensions'


class Grup(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grup'


class Grupespecie(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idespecieinvasora', unique=True, blank=True, null=True)
    idgrup = models.ForeignKey(Grup, models.DO_NOTHING, db_column='idgrup', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupespecie'


class Habitat(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    habitat = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habitat'


class Habitatespecie(models.Model):
    idspinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idspinvasora', blank=True, null=True)
    idhabitat = models.ForeignKey(Habitat, models.DO_NOTHING, db_column='idhabitat', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'habitatespecie'


class Imatge(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    idimatge = models.ForeignKey('Imatges', models.DO_NOTHING, db_column='idimatge', blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imatge'


class Imatges(models.Model):
    idimatge = models.CharField(primary_key=True, max_length=100)
    titol = models.CharField(max_length=4000, blank=True, null=True)
    observacions = models.CharField(max_length=500, blank=True, null=True)
    idextensio = models.ForeignKey(Extensions, models.DO_NOTHING, db_column='idextensio', blank=True, null=True)
    nomoriginal = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.BinaryField(blank=True, null=True)
    fitxer = models.BinaryField(blank=True, null=True)
    visualitzable = models.CharField(max_length=1, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imatges'


class Layer(models.Model):
    topology = models.ForeignKey('Topology', models.DO_NOTHING, primary_key=True)
    layer_id = models.IntegerField()
    schema_name = models.CharField(max_length=-1)
    table_name = models.CharField(max_length=-1)
    feature_column = models.CharField(max_length=-1)
    feature_type = models.IntegerField()
    level = models.IntegerField()
    child_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer'
        unique_together = (('topology', 'layer_id'), ('schema_name', 'table_name', 'feature_column'),)


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


class Nomvulgar(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nomvulgar = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'nomvulgar'


class Nomvulgartaxon(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idtaxon = models.ForeignKey('Taxon', models.DO_NOTHING, db_column='idtaxon')
    idnomvulgar = models.ForeignKey(Nomvulgar, models.DO_NOTHING, db_column='idnomvulgar')
    idnomvulgar_eng = models.ForeignKey(Nomvulgar, models.DO_NOTHING, db_column='idnomvulgar_eng', blank=True, null=True)
    idnomvulgar_es = models.ForeignKey(Nomvulgar, models.DO_NOTHING, db_column='idnomvulgar_es', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nomvulgartaxon'


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
    quadre = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'quadricula'


class Regionativa(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    idzonageografica = models.ForeignKey('Zonageografica', models.DO_NOTHING, db_column='idzonageografica', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regionativa'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


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


class Taxonomia(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    taxonomia = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxonomia'


class Taxonomiataxon(models.Model):
    idtaxonomia = models.ForeignKey(Taxonomia, models.DO_NOTHING, db_column='idtaxonomia', blank=True, null=True)
    idtaxon = models.ForeignKey(Taxon, models.DO_NOTHING, db_column='idtaxon', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taxonomiataxon'


class Topology(models.Model):
    name = models.CharField(unique=True, max_length=-1)
    srid = models.IntegerField()
    precision = models.FloatField()
    hasz = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'topology'


class Viaentrada(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    viaentrada = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viaentrada'


class Viaentradaespecie(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    idespecieinvasora = models.ForeignKey(Especieinvasora, models.DO_NOTHING, db_column='idespecieinvasora', blank=True, null=True)
    idviaentrada = models.ForeignKey(Viaentrada, models.DO_NOTHING, db_column='idviaentrada', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'viaentradaespecie'


class Zonageografica(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    nom = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'zonageografica'

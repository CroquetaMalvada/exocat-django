# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# class Projectes(models.Model):
#     id_projecte = models.DecimalField(db_column='ID_PROJECTE', max_digits=10, decimal_places=0,primary_key=True, )  # Quitado el pk.generaPkProjecte() porque solo se ejecuta una vez al iniciar el servidor
#     #id_projecte = models.AutoField(db_column='ID_PROJECTE', primary_key=True, )  # Field name made lowercase.
#     #id_resp = models.DecimalField(db_column='ID_RESP', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_prj = models.DecimalField(db_column='CODI_PRJ', max_digits=10, decimal_places=0)  # Field name made lowercase.
#     codi_oficial = models.CharField(db_column='CODI_OFICIAL', max_length=255, blank=True)  # Field name made lowercase.
#     titol = models.CharField(db_column='TITOL', max_length=255, blank=True)  # Field name made lowercase.
#     acronim = models.CharField(db_column='ACRONIM', max_length=255, blank=True)  # Field name made lowercase.
#     resum = models.TextField(db_column='RESUM', blank=True)  # Field name made lowercase.
#     comentaris = models.TextField(db_column='COMENTARIS', blank=True)  # Field name made lowercase.
#     data_inici_prj = models.DateTimeField(db_column='DATA_INICI_PRJ', blank=True, null=True)  # Field name made lowercase.
#     data_fi_prj = models.DateTimeField(db_column='DATA_FI_PRJ', blank=True, null=True)  # Field name made lowercase.
#     # id_categoria = models.DecimalField(db_column='ID_CATEGORIA', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     serv_o_subven = models.CharField(db_column='SERV_O_SUBVEN', max_length=1, blank=True) # Field name made lowercase.
#     canon_oficial = models.DecimalField(db_column='CANON_OFICIAL', max_digits=17, decimal_places=2, blank=True, null=True,default=0)  # Field name made lowercase.
#     percen_canon_creaf = models.DecimalField(db_column='PERCEN_CANON_CREAF', max_digits=7, decimal_places=4, blank=True, null=True,default=0)  # Field name made lowercase.
#     percen_iva = models.DecimalField(db_column='PERCEN_IVA', max_digits=7, decimal_places=4, blank=True, null=True,default=0)  # Field name made lowercase.
#     es_docum_web = models.CharField(db_column='ES_DOCUM_WEB', max_length=1, blank=True)  # Field name made lowercase.
#     data_docum_web = models.DateField(db_column='DATA_DOCUM_WEB', blank=True, null=True)  # QUIZAS HAYA QUE USAR DATEFIELD!!!.
#     # id_estat_prj = models.DecimalField(db_column='ID_ESTAT_PRJ', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     es_coordinat = models.CharField(db_column='ES_COORDINAT', max_length=1, blank=True)  # Field name made lowercase.
#     # id_usuari_extern = models.DecimalField(db_column='ID_USUARI_EXTERN', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     convocatoria = models.CharField(db_column='CONVOCATORIA', max_length=255, blank=True)  # Field name made lowercase.
#     resolucio = models.CharField(db_column='RESOLUCIO', max_length=255, blank=True)  # Field name made lowercase.
#
#     #MANY TO MANY
#     usuaris_projecte = models.ManyToManyField(TUsuarisXarxa, through='PrjUsuaris')
#     #organismes_projecte = models.ManyToManyField(TOrganismes, through='PrjUsuaris')
#     centres_participants = models.ManyToManyField(TOrganismes, through='CentresParticipants')
#
#     #FOREIGN KEYS
#     id_resp = models.ForeignKey(Responsables,related_name="responsable_de",db_column='ID_RESP')
#     id_categoria = models.ForeignKey(TCategoriaPrj,related_name="categoria_de",db_column='ID_CATEGORIA')
#     id_estat_prj = models.ForeignKey(TEstatPrj,related_name="estat_de",db_column='ID_ESTAT_PRJ')
#     id_usuari_extern = models.ForeignKey(TUsuarisExterns,related_name="extern_de",db_column='ID_USUARI_EXTERN',null=True, blank=True)
#
#
#     class Meta:
#         managed = False
#         db_table = 'PROJECTES'


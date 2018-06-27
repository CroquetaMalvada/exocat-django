# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea, TextInput, Select, EmailInput, NumberInput
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import *
from exocatsite.models import *

class CitacionsACAForm(forms.ModelForm):
    # opciones_aca = [(massa.codi_aca, massa.nom) for massa in MassesAigua.objects.all().values("nom", "codi_aca")]
    class Meta:
        model = CitacionsACA
        fields = [
            'nom_especie',
            'codi_ma',
            'codi_especie',
            'data_cita',
            'nom_ma',
            'grup',
            'categoria_aca',
            'utm_x',
            'utm_y',
            'localitzacio',
            'autor_cita',
            'font_cita',
            'observacions',
            # 'codi_aca',
            # 'utmx_etrs89',
            # 'utmy_etrs89',
            # 'localitzacio',
            # 'codi_sp',
            # 'data_cita',
            # 'autor_cita',
            # 'font_cita',
            # 'observacions'
        ]
        # widgets = {
        #     'codi_aca': forms.ChoiceField(choices=opciones_aca),
        #
        # }

class CitacionsEspeciesForm(forms.ModelForm):

    class Meta:
        model = CitacionsEspecie
        # choices_especies = [(especie.id, especie.idtaxon__genere) for especie in Especieinvasora.objects.all().order_by("idtaxon__genere").values("id","idtaxon__genere","idtaxon__especie")]
        fields = [
            #'id',
            'especie',
            'idspinvasora',
            'data',
            'comarca',
            'municipi',
            'localitat',
            'finca',
            'paratge',
            'utmx',
            'utmy',
            'utmz',
            'utm_10',
            'utm_1',
            'propietari_nom',
            'adreca',
            'poblacio',
            'telefon',
            'qual_terreny',
            'espai_natural_protegit',
            'espai_nom',
            'superficie_ocupada',
            'presencia',
            'estat_invasio',
            'observacions',
            'grup',
            'contacte',
            'NIP',
            'usuari',
            # 'imatges',
            # 'mapas'
        ]
        widgets = {
            #'idspinvasora': HiddenInput
            'qual_terreny': RadioSelect(choices=(('Forestal','Forestal'),('Agricola','Agrícola'),('Urba','Urbà'))),
            'presencia': RadioSelect(choices=(('A', '< 25'),('B', '25-100'),('C', '100-500'),('D', '> 500'))),
            'observacions': Textarea(),
            'contacte': EmailInput(),
            # 'imatges': ClearableFileInput(attrs={'multiple':True}),
            # 'mapas': ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'especie': 'Nom'
        }

        # def __init__(self, *args, **kwargs):
        #     super(CitacionsEspeciesForm, self).__init__(*args, **kwargs)
        #     for field in self.fields:
        #         field.widget.attrs['class'] = 'form-control'

class ImatgesCitacionsEspecieForm(forms.ModelForm):
    class Meta:
        model = ImatgesCitacions
        fields = ('fitxer', 'tipus')
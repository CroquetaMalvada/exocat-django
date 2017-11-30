# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def view_base_dades(request):
    context = {'especies_invasores': "", 'titulo': "ESPECIES INVASORES"}
    return render(request, 'exocat/base_dades.html', context)
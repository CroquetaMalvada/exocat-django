"""exocat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from exocatsite import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^base_dades/',views.view_base_dades,name="base dades"),
    url(r'^mapa/',views.view_mapa,name="mapa"),
    # AJAX
    url('^ajax_grups_select/', views.json_select_groups),
    url('^ajax_viaentrada_select/', views.json_select_viaentrada),
    url('^ajax_estatus_select/', views.json_select_estatus),
    url('^ajax_regionativa_select/', views.json_select_regionativa),
    #AJAX DATATABLES
    url('^ajax_taula_especies/', views.json_taula_especies),
    url('^ajax_taula_especies_filtres/', views.json_taula_especies_filtres), #Para los filtros
    url('^ajax_mostrar_info_especies/', views.json_info_especie),
    #AJAX PARA MAPA
    url('^especies_seleccion/', views.json_especies_de_seleccion),

]

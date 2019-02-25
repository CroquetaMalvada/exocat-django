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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from exocatsite import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/base_dades/'},name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^base_dades/',views.view_base_dades,name="base dades"),
    url(r'^formularis_localitats_especie/',views.view_formularis_localitats_especie,name="formularis localitats especie"),
    #url(r'^formularis_aca/',views.view_formularis_aca,name="formularis aca"),
    url(r'^formularis/',views.view_formularis_usuari,name="formularis usuari"),
    url(r'^revisar_citacions_aca/',views.view_revisar_citacions_aca,name="revisar citacions aca"),
    url(r'^introduccio_citacions_fitxer/',views.view_introduccio_citacions_fitxer,name="introduccio citacions fitxer"),
    url(r'^mapa/',views.view_mapa,name="mapa"),
    # AJAX SELECTS BASE DE DADES
    url('^ajax_varietat_select/', views.json_select_varietat),
    url('^ajax_grups_select/', views.json_select_groups),
    url('^ajax_viaentrada_select/', views.json_select_viaentrada),
    # url('^ajax_estatus_select/', views.json_select_estatus),
    url('^ajax_estatus_catalunya_select/', views.json_select_estatus_cat),
    url('^ajax_estatus_historic_select/', views.json_select_estatus_historic),
    url('^ajax_regionativa_select/', views.json_select_regionativa),
    #AJAX DATATABLES
    url('^ajax_taula_especies/', views.json_taula_especies),
    url('^ajax_taula_especies_filtres/', views.json_taula_especies_filtres), #Para los filtros
    url('^ajax_mostrar_info_especies/', views.json_info_especie),
    #AJAX PARA MAPA
    url('^especies_de_cuadro/', views.json_especies_de_cuadro),
    url('^especies_de_comarca/', views.json_especies_de_comarca),
    url('^especies_seleccion/', views.json_especies_de_seleccion),
    url('^geometries_punts/', views.json_geometries_punts),
    #AJAX PARA FORMULARIOS
    url('^ajax_formularis_usuari/', views.json_taula_formularis_usuari),
    url('^ajax_revisar_citacions_aca/', views.json_taula_revisar_citacions_aca),
    url('^revisar_citacio_especie_aca/', views.post_revisar_citacions_aca),

    #UPLOAD IMAGEN
    url('^upload_imatge_citacions_especie/$', views.view_upload_imatge_citacions_especie),

    #BORRAR IMAGEN
    url('^delete_imatge_citacions_especie/$', views.view_delete_imatge_citacions_especie),

    #GENERAR CSV
    url('^generar_csv_especies/$', views.generar_csv_especies),

    #GENERAR INFORME CSV CON ESPECIES Y CITACIONES DE CADA UTM 10KM
    url('^generar_csv_informe_utm10/$', views.generar_csv_informe_utm10),

    #GENERAR PLANTILLA CSV
    url('^generar_plantilla_citacions/$', views.generar_csv_plantilla_citaciones),

    #UPLOAD ARCHIVO CITACIONES
    url('^upload_citaciones_csv/$', views.upload_citaciones_csv),
]
# solo para desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

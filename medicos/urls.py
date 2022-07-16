import statistics
from django.conf import settings
from django.urls import path, re_path
#now import the views.py file into this code

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, register_converter
from medicos.converters import DateConverter
from .views import *

register_converter(DateConverter, 'date')

app_name = 'medicos'
urlpatterns=[
    path('', helloDoctors, name='menu_medico'),
    re_path('agregar-paciente/', agregar_pacientes, name='agregar_paciente'),
    re_path('editar-doctor/', editar_doctor, name='editar_doctor'),
    re_path('diagnostico-anonimo/', diagnostico_anonimo, name='diagnostico_anonimo'),
    re_path('aceptar-resultado/(?P<id>\d+)/(?P<res>\d+)/$', aceptar_resultado_paciente, name='aceptar_resultado_paciente'),
    re_path('rechazar-resultado/(?P<id>\d+)/(?P<res>\d+)/$', rechazar_resultado_paciente, name='rechazar_resultado_paciente'),
    re_path('generar-diagnostico/', diagnostico_pacientes, name='generar_diagnostico'),
    re_path('generar-diagnostico-multiple/', diagnostico_multiple, name='generar_diagnostico-multiple'),
    re_path('generar-diagnostico-paciente/(?P<id>\d+)/$', diagnosticar_paciente, name='diagnosticar_paciente'),
    re_path('generar-pdf-paciente/(?P<id>\d+)/(?P<pk_2>\d+)/$', generar_pdf_individual_momentaneo, name='generar_pdf_individual_momentaneo'),
    re_path('listar-pacientes/', listar_pacientes, name='listar_pacientes'),
    re_path('listar-resultados/', listar_resultados, name='listar_resultados'),
    re_path('eliminar-paciente/(?P<id>\d+)/$', eliminar_paciente, name='eliminar_paciente'),
    re_path('actualizar-paciente/(?P<id>\d+)/$', actualizar_paciente_uno, name='actualizar_paciente'),
    re_path('generar-reporte-paciente/(?P<id>\d+)/(?P<pk_2>\d+)/(?P<pk_3>\d+)/$', generar_pdf_individual, name='generar_reporte_individual'),
    re_path('generar-reporte-multiple/', generar_pdf_multiple, name='generar_pdf_multiple'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
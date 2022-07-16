from django.urls import path, re_path
#now import the views.py file into this code
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = 'pacientes'
urlpatterns=[
    path('', helloPacientes, name='menu_pacientes'),

    #re_path('actualizar-paciente/(?P<id>\d+)/$', actualizar_paciente, name='actualizar_paciente'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                            document_root=settings.MEDIA_ROOT)

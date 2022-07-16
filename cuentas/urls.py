from django.urls import path
from .import  views

urlpatterns=[
    path('registro/',views.register, name='register'),
    #path('registro_paciente/',views.Paciente_register.as_view(), name='paciente_registro'),
    path('registro_medico/',views.Medico_register.as_view(), name='medico_registro'),
    path('login/',views.login_request, name='login'),
    path('logout/',views.logout_view, name='logout'),
]
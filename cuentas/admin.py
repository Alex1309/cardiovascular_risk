from django.contrib import admin
from .models import User
from pacientes.models import Paciente
from medicos.models import Medico

admin.site.register(User)
admin.site.register(Paciente)
admin.site.register(Medico)


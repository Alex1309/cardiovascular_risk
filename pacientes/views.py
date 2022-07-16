import http
from django.shortcuts import get_object_or_404, render

from cuentas.models import User
from medicos.models import ResultadoPaciente
from .forms import PacienteForm
from .models import Paciente
# Create your views here.


def helloPacientes(request):
    
    username_paciente = request.user.nombre
    resultados_lista = ResultadoPaciente.objects.filter(paciente_id=request.user.id)
    paciente_imagen = Paciente.objects.get(user__id=request.user.id)
    return render(request, "pacientes.html",{'nombre_paciente':username_paciente, 'resultados':resultados_lista,'paciente_imagen':paciente_imagen})


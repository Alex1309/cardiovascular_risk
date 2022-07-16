from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import PacienteSignUpForm, MedicoSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

def register(request):
    return render(request, '../templates/register.html')

class Medico_register(CreateView):
    model = User
    form_class = MedicoSignUpForm
    template_name = '../templates/medico_registro.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class Paciente_register(CreateView):
    model = User
    form_class = PacienteSignUpForm
    template_name = '../templates/paciente_registro.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_medico:
                login(request,user)
                return redirect('/medicos/')
            elif user is not None and user.is_paciente:
                login(request, user)
                print(user.nombre)
                print('gracias')
                return redirect('/pacientes/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',
    context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


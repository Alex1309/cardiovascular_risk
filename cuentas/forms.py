from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import AbstractUser
from pacientes.models import Paciente
from medicos.models import Medico
from .models import User
SEXO_CHOICES =(
    (1, "Femenino"),
    (2, "Masculino"),

)
DIABETES_CHOICES =(
    (1, "Si"),
    (0, "No"),

)
TABACO_CHOICES =(
    (1, "Si"),
    (0, "No"),

)
ANTECEDENTES_CHOICES =(
    (1, "Si"),
    (0, "No"),

)
TIPO_SANGRE_CHOICES =(
    ("A+", "A+"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)
class MedicoSignUpForm(UserCreationForm):
    nombre = forms.CharField(required=True)
    apellido = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    identidad = forms.CharField(required=True)
    #direccion = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    #edad = forms.IntegerField(required=True)
    #tipo_sangre = forms.ChoiceField(required=True,choices=TIPO_SANGRE_CHOICES)
    #sexo = forms.ChoiceField(required=True,choices =SEXO_CHOICES)
    #Peso = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    #talla =models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    #diabetes = models.IntegerField(blank=True, null=True)
    #presion_sistolica = models.IntegerField(blank=True, null=True)
    #presion_diastolica = models.IntegerField(blank=True, null=True)
    #colesterol_total = models.IntegerField(blank=True, null=True)
    #hdl = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    #ldl = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    #triglicerios = models.IntegerField(blank=True, null=True)
    #tabaquismo = models.IntegerField(blank=True, null=True)
    #antecedentes = models.IntegerField(blank=True, null=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_medico = True
        user.is_staff = True
        user.nombre = self.cleaned_data.get('nombre')
        user.apellido = self.cleaned_data.get('apellido')
        user.save()
        medico = Medico.objects.create(user=user)
        medico.identidad=self.cleaned_data.get('identidad')
        medico.telefono=self.cleaned_data.get('telefono')
        medico.email=self.cleaned_data.get('email')
        medico.nombre =user.nombre
        medico.apellido =user.apellido

        #medico.direccion=self.cleaned_data.get('direccion')
        #medico.edad=self.cleaned_data.get('edad')
        #medico.tipo_sangre=self.cleaned_data.get('tipo_sangre')
        #medico.sexo=self.cleaned_data.get('sexo')
        medico.save()
        return user

class PacienteSignUpForm(UserCreationForm):
    nombre = forms.CharField(required=True)
    apellido = forms.CharField(required=True)


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_paciente = True
        user.nombre = self.cleaned_data.get('nombre')
        user.apellido = self.cleaned_data.get('apellido')
        user.save()
        paciente = Paciente.objects.create(user=user)
        paciente.save()
        return user

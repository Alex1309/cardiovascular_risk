from cgitb import handler
from functools import total_ordering
from tkinter import image_names
from tokenize import PseudoExtras
from xmlrpc.client import ServerProxy
from django.db import models
from django.forms import PasswordInput
from pacientes.models import Paciente
from cuentas.models import User
from django.utils.timezone import now

SEXO_CHOICES =(
    (1, "Femenino"),
    (2, "Masculino"),

)
DIABETES_CHOICES =(
    (1, "Si"),
    (0, "No"),

)
RESULTADO_CHOICES =(
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

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=50)
    identidad = models.CharField(max_length=100)
    paciente = models.ManyToManyField('pacientes.Paciente', related_name='medicos')
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    imagen =  models.ImageField(upload_to ='uploads/',blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    tipo_sangre = models.CharField(max_length=10,choices=TIPO_SANGRE_CHOICES)
    departamento = models.CharField(max_length=100,blank=True, null=True)
    sexo = models.IntegerField(blank=True, null=True,choices=SEXO_CHOICES)
    Peso = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    talla =models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    diabetes = models.IntegerField(blank=True, null=True,choices=DIABETES_CHOICES)
    presion_sistolica = models.IntegerField(blank=True, null=True)
    presion_diastolica = models.IntegerField(blank=True, null=True)
    colesterol_total = models.IntegerField(blank=True, null=True)
    hdl = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    ldl = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True, null=True)
    triglicerios = models.IntegerField(blank=True, null=True)
    tabaquismo = models.IntegerField(blank=True, null=True,choices=TABACO_CHOICES)
    antecedentes = models.IntegerField(blank=True, null=True,choices=ANTECEDENTES_CHOICES)
    class Meta:  
        db_table = "medico"

class Resultado(models.Model):
    resultado = models.CharField(max_length=5,choices=RESULTADO_CHOICES)

class ResultadoPaciente(models.Model):
    paciente = models.ForeignKey('pacientes.Paciente',on_delete = models.CASCADE, related_name='resultados')
    resultado_paciente = models.ForeignKey('medicos.Resultado',on_delete = models.CASCADE, related_name='resultados_paciente')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:  
        db_table = "resultado_paciente"


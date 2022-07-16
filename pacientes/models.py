from cgitb import handler
from functools import total_ordering
from subprocess import check_output
from tkinter import image_names
from tokenize import PseudoExtras
from xmlrpc.client import ServerProxy
from django.db import models
from django.forms import PasswordInput
from cuentas.models import User

# Create your models here.

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
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    password = models.CharField(max_length=50)
    identidad = models.CharField(max_length=600,blank=True,null=True)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    imagen =  models.ImageField(upload_to ='uploads/',blank=True,null=True)
    resultado =  models.CharField(max_length=500,blank=True,null=True)
    edad = models.IntegerField(blank=True,null=True)
    tipo_sangre = models.CharField(max_length=10,choices=TIPO_SANGRE_CHOICES)
    sexo = models.IntegerField(choices=SEXO_CHOICES,blank=True,null=True)
    Peso = models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True,null=True)
    talla =models.DecimalField(default=0, max_digits=5, decimal_places=2,blank=True,null=True)
    diabetes = models.IntegerField(choices=DIABETES_CHOICES,blank=True,null=True)
    presion_sistolica = models.IntegerField(blank=True,null=True)
    presion_diastolica = models.IntegerField(blank=True,null=True)
    colesterol_total = models.IntegerField(blank=True,null=True)
    hdl = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    ldl = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    triglicerios = models.IntegerField(blank=True,null=True)
    tabaquismo = models.IntegerField(choices=TABACO_CHOICES,blank=True,null=True)
    antecedentes = models.IntegerField(choices=ANTECEDENTES_CHOICES,blank=True,null=True)
    class Meta:  
        db_table = "paciente"
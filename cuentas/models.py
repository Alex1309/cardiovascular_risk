from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_paciente = models.BooleanField(default=False)
    is_medico = models.BooleanField(default=False)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
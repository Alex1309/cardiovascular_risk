from django import forms  
from pacientes.models import Paciente 
import re
from django.core.validators import RegexValidator
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType


class PacienteForm(forms.ModelForm):  
    password = forms.CharField(widget=forms.PasswordInput)
    Peso = forms.DecimalField(min_value=1, required=False)
    talla = forms.DecimalField(min_value=1, required=False)
    edad = forms.IntegerField(min_value=1, required=False)
    hdl = forms.DecimalField(min_value=1, required=False)
    ldl = forms.DecimalField(min_value=1, required=False)
    presion_sistolica = forms.IntegerField(min_value=1, required=False)
    presion_diastolica = forms.IntegerField(min_value=1, required=False)
    colesterol_total = forms.IntegerField(min_value=1, required=False)
    triglicerios = forms.IntegerField(min_value=1, required=False)
    #fecha_nacimiento =forms.DateField(widget = forms.SelectDateWidget())
    telefono = forms.CharField(validators=[RegexValidator('[1-9][0-9]{9}', message="El telefono no puede contener letras y debe tener 10 digitos")])
    identidad = forms.CharField(validators=[RegexValidator('^\d\d\d[0-9]*$', message="La cedula no puede contener letras y debe tener al menos 3 digitos")])

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        if True in [char.isdigit() for char in nombre] and len(nombre) < 3 :
            msg = "El nombre no puede contener números y tener menos de 3 letras."
            self.add_error('nombre', msg)
        if True in [char.isdigit() for char in apellido] and len(apellido) < 3:
            msg = "El apellido no puede contener números y tener menos de 3 letras."
            self.add_error('apellido', msg)


    class Meta:  
        model = Paciente 
        #permissions = [('can_eat_pizzas')]

        fields =  ['nombre', 'apellido', 'email', 'password','identidad','direccion','telefono','imagen','edad',
        'tipo_sangre','sexo','Peso','talla','diabetes','presion_sistolica','presion_diastolica','colesterol_total','hdl','ldl','triglicerios','tabaquismo','antecedentes']

        #content_type = ContentType.objects.get_for_model(Paciente, for_concrete_model=False)
        #paciente_permissions = Permission.objects.filter(content_type=content_type)
        #for permission in paciente_permissions:
        #s    User.user_permissions.add(permission)

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['imagen'].required = False
        self.fields['password'].required = False
        #self.fields['imagen'].widget.attrs.update({'class': 'form-control custom-file-input','id': 'validatedCustomFile'})


from django import forms  
from medicos.models import Medico  
from django.core.validators import RegexValidator

class MedicoForm(forms.ModelForm):  
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
        model = Medico  
        fields = ['nombre', 'apellido', 'email','identidad','departamento','direccion','telefono','imagen','edad',
        'tipo_sangre','sexo','Peso','talla','diabetes','presion_sistolica','presion_diastolica','colesterol_total','hdl','ldl','triglicerios','tabaquismo','antecedentes']


    def __init__(self, *args, **kwargs):
        super(MedicoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            #self.fields['imagen'].widget.attrs.update({'class': 'custom-file-label'})
        self.fields['imagen'].required = False
        self.fields['password'].required = False
        self.fields['direccion'].required = False
        self.fields['tipo_sangre'].required = False
        self.fields['departamento'].required = False
        self.fields['sexo'].required = False
        self.fields['diabetes'].required = False
        self.fields['antecedentes'].required = False
        self.fields['tabaquismo'].required = False
        #self.fields['imagen'].widget.attrs.update({'class': 'form-control custom-file-input','id': 'validatedCustomFile'})

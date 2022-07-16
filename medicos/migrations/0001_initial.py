# Generated by Django 4.0.4 on 2022-06-07 23:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cuentas', '0001_initial'),
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resultado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultado', models.CharField(choices=[(1, 'Si'), (0, 'No')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados', to='pacientes.paciente')),
                ('resultado_paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultados_paciente', to='medicos.resultado')),
            ],
            options={
                'db_table': 'resultado_paciente',
            },
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=75)),
                ('password', models.CharField(max_length=50)),
                ('identidad', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('tipo_sangre', models.CharField(choices=[('A+', 'A+'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=10)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
                ('sexo', models.IntegerField(blank=True, choices=[(1, 'Femenino'), (2, 'Masculino')], null=True)),
                ('Peso', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('talla', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('diabetes', models.IntegerField(blank=True, choices=[(1, 'Si'), (0, 'No')], null=True)),
                ('presion_sistolica', models.IntegerField(blank=True, null=True)),
                ('presion_diastolica', models.IntegerField(blank=True, null=True)),
                ('colesterol_total', models.IntegerField(blank=True, null=True)),
                ('hdl', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('ldl', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
                ('triglicerios', models.IntegerField(blank=True, null=True)),
                ('tabaquismo', models.IntegerField(blank=True, choices=[(1, 'Si'), (0, 'No')], null=True)),
                ('antecedentes', models.IntegerField(blank=True, choices=[(1, 'Si'), (0, 'No')], null=True)),
                ('paciente', models.ManyToManyField(related_name='medicos', to='pacientes.paciente')),
            ],
            options={
                'db_table': 'medico',
            },
        ),
    ]
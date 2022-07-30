from this import d
import uuid
import pytz
from django import http
from django.contrib import messages  # import messages
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from joblib import load
from pacientes.models import Paciente
from cuentas.models import User
from medicos.models import Medico, Resultado, ResultadoPaciente
from .forms import MedicoForm
from pacientes.forms import PacienteForm
from fpdf import FPDF
import pandas as pd
import io
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
# Create your views here.


def helloDoctors(request):

    username_doctor = request.user.nombre
    medico_imagen = Medico.objects.get(user__id=request.user.id)
    return render(request, "doctores.html", {'nombre_doctor': username_doctor, 'medico_imagen': medico_imagen})


def listar_resultados(request):
    pacientes = Paciente.objects.all()
    imagen = Medico.objects.get(user__id=request.user.id)
    pacientes_por_medico = Medico.objects.get(
        user__id=request.user.id).paciente.all()
    ids_pacientes = pacientes_por_medico.values_list('user_id', flat=True)
    resultados_lista = ResultadoPaciente.objects.filter(
        paciente__in=ids_pacientes)
    username_doctor = request.user.nombre
    return render(request, 'listar-resultados.html', {'resultados': resultados_lista, 'nombre_doctor': username_doctor, 'medico_imagen': imagen})


def generar_pdf_anonimo(request):

    nameFile = ""
    pdf = FPDF('P', 'mm', 'A4')

    values_pacientes = request.session.get('values_paciente_anonimo')
    edad = int(values_pacientes[0])
    sexo = int(values_pacientes[1])
    peso = int(values_pacientes[2])
    talla = int(values_pacientes[3])
    diabetes = int(values_pacientes[4])
    sistolica = int(values_pacientes[5])
    diastolica = int(values_pacientes[6])
    colesterol = int(values_pacientes[7])
    hdl = float(values_pacientes[8])
    ldl = float(values_pacientes[9])
    triglicerios = int(values_pacientes[10])
    tabaco = int(values_pacientes[11])
    antecedentes = int(values_pacientes[12])
    res =str(values_pacientes[13])
    if sexo == 1:
        sexo = "Masculino"
    else:
        sexo = "Femenino"

    if diabetes ==1:
        diabetes = "Sí"
    else:
        diabetes = "No"

    if tabaco ==1:
        tabaco = "Sí"
    else:
        tabaco = "No"
    if antecedentes ==1:
        antecedentes = "Sí"
    else:
        antecedentes = "No"

    result = ""
    if(res!="No tiene riesgo cardiovascular"):
        result = "presenta riesgo Cardiovascular."
    else:
        result = "no presenta riesgo Cardiovascular."

    time_colombia = pytz.timezone("America/Bogota")
    final_time = datetime.now().astimezone(time_colombia)    
    formatedDate = final_time.strftime("%Y-%m-%d %H:%M:%S")
    sales = [
        {"item": "Edad:", "amount": str(edad)},
        {"item": "Sexo:", "amount": sexo},
        {"item": "Peso:", "amount": str(peso)},
        {"item": "Talla:", "amount": str(talla)},
        {"item": "Diabetes:", "amount": diabetes},
        {"item": "Presion sistolica:", "amount": str(sistolica)},
        {"item": "Presion diastolica:", "amount": str(diastolica)},
        {"item": "Colesterol total:", "amount": str(colesterol)},
        {"item": "Hdl:", "amount": str(hdl)},
        {"item": "Ldl:", "amount": str(ldl)},
        {"item": "Triglicerios:", "amount": str(triglicerios)},
        {"item": "Tabaquismo:", "amount": tabaco},
        {"item": "Antecedentes:", "amount": antecedentes},
    ]
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(190, 10, 'Reporte PDF - Diagnóstico Anónimo', 0, 0, 'C')
    pdf.cell(40, 10, '',0,1)
    pdf.cell(40, 10, '',0,1)

    pdf.set_font('courier', '', 12)
    pdf.cell(0,10, f"{'Datos'.ljust(30)} {'Información personal'.rjust(20)}", 0, 0, 'C')
    pdf.line(10, 30, 200, 30)
    pdf.line(10, 38, 200, 38)

    pdf.cell(ln=1, h=15.0, align='L', w=0, txt="", border=0)
    pdf.cell(0,10, f"{'Fecha'.ljust(30)} {str(formatedDate).rjust(20)}", 0, 1, 'C')
    pdf.line(40, 54, 170, 54)

    for line in sales:
        pdf.cell(0,10, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1,'C')
    pdf.cell(ln=1, h=12, align='L', w=0, txt="", border=0)
    if result =="no presenta riesgo Cardiovascular.":
        pdf.set_text_color(92, 190, 21) 
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')
    else:
        pdf.set_text_color(255,0,0)   
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')

    nameFile= formatedDate
    nameFile+=".pdf"
    pdf.output(nameFile, 'F')
    return FileResponse(open(nameFile, 'rb'), as_attachment=True, content_type='application/pdf')

def generar_pdf_multiple(request):

    ids_resultados = request.session.get('values')
    pdf = FPDF('P', 'mm', 'A4')
    nameFile=""
    for value in ids_resultados:
        user = get_object_or_404(Paciente, user_id=value['id_paciente'])
        sexo = ""
        if user.sexo ==1:
            sexo = "Femenino"
        else:
            sexo = "Masculino"
        diabetes = ""
        if user.diabetes ==1:
            diabetes = "Sí"
        else:
            diabetes = "No"
        tabaquismo = ""
        if user.tabaquismo ==1:
            tabaquismo = "Sí"
        else:
            tabaquismo = "No"
        antecedentes =""
        if user.antecedentes ==1:
            antecedentes = "Sí"
        else:
            antecedentes = "No"
        result = ""
        if(value['respuesta']=="Si tiene riesgo cardiovascular"):
            result = "presenta riesgo Cardiovascular."
        else:
            result = "no presenta riesgo Cardiovascular."
        fecha = ResultadoPaciente.objects.get(pk=value['resultado_id']).create_time
        time_colombia = pytz.timezone("America/Bogota")
        final_time = fecha.astimezone(time_colombia)    
        formatedDate = final_time.strftime("%Y-%m-%d %H:%M:%S")
        sales = [
            {"item": "Nombre:", "amount": user.nombre},
            {"item": "Apellido:", "amount": user.apellido},
            {"item": "Email:", "amount": user.email},
            {"item": "Cedula:", "amount": user.identidad},
            {"item": "Edad:", "amount": str(user.edad)},
            {"item": "Sexo:", "amount": sexo},
            {"item": "Peso:", "amount": str(user.Peso)},
            {"item": "Talla:", "amount": str(user.talla)},
            {"item": "Diabetes:", "amount": diabetes},
            {"item": "Presion sistolica:", "amount": str(user.presion_sistolica)},
            {"item": "Presion diastolica:", "amount": str(user.presion_diastolica)},
            {"item": "Colesterol total:", "amount": str(user.colesterol_total)},
            {"item": "Hdl:", "amount": str(user.hdl)},
            {"item": "Ldl:", "amount": str(user.ldl)},
            {"item": "Triglicerios:", "amount": str(user.triglicerios)},
            {"item": "Tabaquismo:", "amount": tabaquismo},
            {"item": "Antecedentes:", "amount": antecedentes},
        ]
        pdf.add_page()
        pdf.set_font('courier', 'B', 16)
        pdf.cell(190, 10, 'Reporte PDF - Diagnóstico Multiple', 0, 0, 'C')
        pdf.cell(40, 10, '',0,1)
        pdf.cell(40, 10, '',0,1)

        pdf.set_font('courier', '', 12)
        pdf.cell(0,10, f"{'Datos'.ljust(30)} {'Información personal'.rjust(20)}", 0, 0, 'C')
        pdf.line(10, 30, 200, 30)
        pdf.line(10, 38, 200, 38)

        pdf.cell(ln=1, h=15.0, align='L', w=0, txt="", border=0)
        pdf.cell(0,10, f"{'Fecha'.ljust(30)} {str(formatedDate).rjust(20)}", 0, 1, 'C')
        pdf.line(40, 54, 170, 54)

        for line in sales:
            pdf.cell(0,10, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1,'C')
        pdf.cell(ln=1, h=12, align='L', w=0, txt="", border=0)
        if result =="no presenta riesgo Cardiovascular.":
            pdf.set_text_color(92, 190, 21) 
            pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')


        else:
            pdf.set_text_color(255,0,0)   
            pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')


        nameFile+= user.nombre+user.identidad+"-"
    nameFile+=".pdf"
    pdf.output(nameFile, 'F')
    return FileResponse(open(nameFile, 'rb'), as_attachment=True, content_type='application/pdf')

def generar_pdf_individual_momentaneo(request,id,pk_2):
    user = Paciente.objects.get(user__id=id)
    resultado = Resultado.objects.create(resultado=int(pk_2))
    resultado_paciente = ResultadoPaciente.objects.create(paciente=user,resultado_paciente=resultado)
    pk_3 = int(resultado_paciente.pk)

    sexo = ""
    if user.sexo ==1:
        sexo = "Femenino"
    else:
        sexo = "Masculino"
    diabetes = ""
    if user.diabetes ==1:
        diabetes = "Sí"
    else:
        diabetes = "No"
    tabaquismo = ""
    if user.tabaquismo ==1:
        tabaquismo = "Sí"
    else:
        tabaquismo = "No"
    antecedentes =""
    if user.antecedentes ==1:
        antecedentes = "Sí"
    else:
        antecedentes = "No"
    result = ""
    print('result',pk_2)
    if(pk_2=="1"):
        result = "presenta riesgo Cardiovascular."
    else:
        result = "no presenta riesgo Cardiovascular."

    fecha = ResultadoPaciente.objects.get(pk=pk_3).create_time
    time_colombia = pytz.timezone("America/Bogota")
    final_time = fecha.astimezone(time_colombia)    
    formatedDate = final_time.strftime("%Y-%m-%d %H:%M:%S")
    sales = [
        {"item": "Nombre:", "amount": user.nombre},
        {"item": "Apellido:", "amount": user.apellido},
        {"item": "Email:", "amount": user.email},
        {"item": "Cedula:", "amount": user.identidad},
        {"item": "Edad:", "amount": str(user.edad)},
        {"item": "Sexo:", "amount": sexo},
        {"item": "Peso:", "amount": str(user.Peso)},
        {"item": "Talla:", "amount": str(user.talla)},
        {"item": "Diabetes:", "amount": diabetes},
        {"item": "Presion sistolica:", "amount": str(user.presion_sistolica)},
        {"item": "Presion diastolica:", "amount": str(user.presion_diastolica)},
        {"item": "Colesterol total:", "amount": str(user.colesterol_total)},
        {"item": "Hdl:", "amount": str(user.hdl)},
        {"item": "Ldl:", "amount": str(user.ldl)},
        {"item": "Triglicerios:", "amount": str(user.triglicerios)},
        {"item": "Tabaquismo:", "amount": tabaquismo},
        {"item": "Antecedentes:", "amount": antecedentes},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(190, 10, 'Reporte PDF - Diagnostico Individual', 0, 0, 'C')
    pdf.cell(40, 10, '',0,1)
    pdf.cell(40, 10, '',0,1)

    pdf.set_font('courier', '', 12)
    pdf.cell(0,10, f"{'Datos'.ljust(30)} {'Información personal'.rjust(20)}", 0, 0, 'C')
    pdf.line(10, 30, 200, 30)
    pdf.line(10, 38, 200, 38)

    pdf.cell(ln=1, h=15.0, align='L', w=0, txt="", border=0)
    pdf.cell(0,10, f"{'Fecha'.ljust(30)} {str(formatedDate).rjust(20)}", 0, 1, 'C')
    pdf.line(40, 54, 170, 54)

    for line in sales:
        pdf.cell(0,10, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1,'C')
    pdf.cell(ln=1, h=12, align='L', w=0, txt="", border=0)

    if result =="no presenta riesgo Cardiovascular.":
        pdf.set_text_color(92, 190, 21)    
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')
    else:
        pdf.set_text_color(255,0,0)    
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')

    nameFile = user.nombre+user.identidad+".pdf"
    pdf.output(nameFile, 'F')
    return FileResponse(open(nameFile, 'rb'), as_attachment=True, content_type='application/pdf')



def generar_pdf_individual(request,id,pk_2,pk_3):

    user = get_object_or_404(Paciente, user_id=id,)

    sexo = ""
    if user.sexo ==1:
        sexo = "Femenino"
    else:
        sexo = "Masculino"
    diabetes = ""
    if user.diabetes ==1:
        diabetes = "Sí"
    else:
        diabetes = "No"
    tabaquismo = ""
    if user.tabaquismo ==1:
        tabaquismo = "Sí"
    else:
        tabaquismo = "No"
    antecedentes =""
    if user.antecedentes ==1:
        antecedentes = "Sí"
    else:
        antecedentes = "No"
    result = ""
    print('result',pk_2)
    if(pk_2=="1"):
        result = "presenta riesgo Cardiovascular."
    else:
        result = "no presenta riesgo Cardiovascular."
    print(type(pk_3))
    fecha = ResultadoPaciente.objects.get(pk=pk_3).create_time
    time_colombia = pytz.timezone("America/Bogota")
    final_time = fecha.astimezone(time_colombia)    
    formatedDate = final_time.strftime("%Y-%m-%d %H:%M:%S")
    sales = [
        {"item": "Nombre:", "amount": user.nombre},
        {"item": "Apellido:", "amount": user.apellido},
        {"item": "Email:", "amount": user.email},
        {"item": "Cedula:", "amount": user.identidad},
        {"item": "Edad:", "amount": str(user.edad)},
        {"item": "Sexo:", "amount": sexo},
        {"item": "Peso:", "amount": str(user.Peso)},
        {"item": "Talla:", "amount": str(user.talla)},
        {"item": "Diabetes:", "amount": diabetes},
        {"item": "Presion sistolica:", "amount": str(user.presion_sistolica)},
        {"item": "Presion diastolica:", "amount": str(user.presion_diastolica)},
        {"item": "Colesterol total:", "amount": str(user.colesterol_total)},
        {"item": "Hdl:", "amount": str(user.hdl)},
        {"item": "Ldl:", "amount": str(user.ldl)},
        {"item": "Triglicerios:", "amount": str(user.triglicerios)},
        {"item": "Tabaquismo:", "amount": tabaquismo},
        {"item": "Antecedentes:", "amount": antecedentes},
    ]
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(190, 10, 'Reporte PDF - Diagnostico Individual', 0, 0, 'C')
    pdf.cell(40, 10, '',0,1)
    pdf.cell(40, 10, '',0,1)

    pdf.set_font('courier', '', 12)
    pdf.cell(0,10, f"{'Datos'.ljust(30)} {'Información personal'.rjust(20)}", 0, 0, 'C')
    pdf.line(10, 30, 200, 30)
    pdf.line(10, 38, 200, 38)

    pdf.cell(ln=1, h=15.0, align='L', w=0, txt="", border=0)
    pdf.cell(0,10, f"{'Fecha'.ljust(30)} {str(formatedDate).rjust(20)}", 0, 1, 'C')
    pdf.line(40, 54, 170, 54)

    for line in sales:
        pdf.cell(0,10, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1,'C')
    pdf.cell(ln=1, h=12, align='L', w=0, txt="", border=0)
    if result =="no presenta riesgo Cardiovascular.":
        pdf.set_text_color(92, 190, 21)  
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')
          
    else:
        pdf.set_text_color(255,0,0)    
        pdf.cell(0, 10, 'El paciente ' + result, 0, 0, 'C')
    nameFile = user.nombre+user.identidad+".pdf"
    pdf.output(nameFile, 'F')
    return FileResponse(open(nameFile, 'rb'), as_attachment=True, content_type='application/pdf')

def diagnostico_pacientes(request):
    username_doctor = request.user.nombre
    pacientes = Paciente.objects.all()
    pacientes_por_medico = Medico.objects.get(user__id=request.user.id).paciente.all()
    imagen = Medico.objects.get(user__id=request.user.id)
    return render(request,'generar-diagnostico.html',{'pacientes':pacientes_por_medico,'nombre_doctor':username_doctor,'medico_imagen':imagen})


def diagnostico_multiple(request):
    
    username_doctor = request.user.nombre
    imagen = Medico.objects.get(user__id=request.user.id)

    pacientes = Paciente.objects.all()
    pacientes_por_medico = Medico.objects.get(user__id=request.user.id).paciente.all()
    values =""
    model = load('./savedModels/modelo_MLP.joblib')
    todos_list=[]
    nombre_paciente=""
    apellido_paciente = ""
    identidad_paciente = ""
    id_resultado_paciente = ""
    id_paciente = ""
    dic ={}
    uplist=[]
    if request.method == "POST": 

        values = request.POST.getlist(u'hola')
        request.session['values_id_pacientes'] = values

        # print('values_checkbox',values)
        pacientes_seleccionados = Paciente.objects.filter(user_id__in=values)
        
        for paciente_diagnosticar in pacientes_seleccionados:
        
            nombre_paciente = (paciente_diagnosticar.nombre)
            apellido_paciente =(paciente_diagnosticar.apellido)
            identidad_paciente =(paciente_diagnosticar.identidad)
            id_paciente = (paciente_diagnosticar.pk)

            edad = int(paciente_diagnosticar.edad)
            sexo = int(paciente_diagnosticar.sexo)
            peso = int(paciente_diagnosticar.Peso)
            talla = int(paciente_diagnosticar.talla)
            diabetes = int(paciente_diagnosticar.diabetes)
            sistolica = int(paciente_diagnosticar.presion_sistolica)
            diastolica = int(paciente_diagnosticar.presion_diastolica)
            colesterol = int(paciente_diagnosticar.colesterol_total)
            hdl = float(paciente_diagnosticar.hdl)
            ldl = float(paciente_diagnosticar.ldl)
            triglicerios = int(paciente_diagnosticar.triglicerios)
            tabaco = int(paciente_diagnosticar.tabaquismo)
            antecedentes=int(paciente_diagnosticar.antecedentes)
            print(paciente_diagnosticar.nombre, edad," ",sexo,peso,talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes)
            y_pred = model.predict([[edad, sexo, peso, talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes]])

            if y_pred[0] == 1:
                y_pred = 'Si tiene riesgo cardiovascular'
                resultado = Resultado.objects.create(resultado=1)
                resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente_diagnosticar,resultado_paciente=resultado)
                id_resultado_paciente =resultado_paciente.id
                uplist.append(id_resultado_paciente)

            else:
                resultado = Resultado.objects.create(resultado=0)
                resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente_diagnosticar,resultado_paciente=resultado)
                y_pred = 'No tiene riesgo cardiovascular'
                # uplist.append(str(resultado_paciente.id))
                id_resultado_paciente =resultado_paciente.id
                uplist.append(id_resultado_paciente)


            dic = {
                'id_paciente': id_paciente,
                'nombre': nombre_paciente,
                'apellido': apellido_paciente,
                'identidad': identidad_paciente,
                'respuesta': y_pred,
                'resultado_id': id_resultado_paciente
            }
            todos_list.append(dic)
        request.session['values'] = todos_list
        request.session['uplist'] = uplist

    return render(request,'generar-diagnostico-multiple.html',{'pacientes':pacientes_por_medico,'nombre_doctor':username_doctor,'todos':todos_list,'medico_imagen':imagen,'uplist': uplist})

def diagnosticar_paciente(request, id=None):
    user_id=id
    paciente_diagnosticar = Paciente.objects.get(user__id=user_id)
    print(paciente_diagnosticar.nombre)
    model = load('./savedModels/modelo_MLP.joblib')
    print("edad "+" sexo "+" peso "+" talla "+" diabetes "+" sistolica "+ " diastolica "+" colesterol"+ " hdl "+" ldl "+ "trig "+" tabaquismo "+" antecedentes ")

    identidad_paciente =paciente_diagnosticar.identidad
    nombre_paciente =paciente_diagnosticar.nombre
    apellido_paciente =paciente_diagnosticar.apellido
    if request.method == 'GET':
        pacientes_por_medico = Medico.objects.get(user__id=request.user.id).paciente.all()
        edad = int(paciente_diagnosticar.edad)
        sexo = int(paciente_diagnosticar.sexo)
        peso = int(paciente_diagnosticar.Peso)
        talla = int(paciente_diagnosticar.talla)
        diabetes = int(paciente_diagnosticar.diabetes)
        sistolica = int(paciente_diagnosticar.presion_sistolica)
        diastolica = int(paciente_diagnosticar.presion_diastolica)
        colesterol = int(paciente_diagnosticar.colesterol_total)
        hdl = float(paciente_diagnosticar.hdl)
        ldl = float(paciente_diagnosticar.ldl)
        triglicerios = int(paciente_diagnosticar.triglicerios)
        tabaco = int(paciente_diagnosticar.tabaquismo)
        antecedentes=int(paciente_diagnosticar.antecedentes)
        print(edad," ",sexo,peso,talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes)
        y_pred = model.predict([[edad, sexo, peso, talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes]])
        # id_resultado = ""
        # 'resultado_id':id_resultado,
        if y_pred[0] == 1:
            y_pred = 'Si tiene riesgo cardiovascular'
            # resultado = Resultado.objects.create(resultado=1)
            # resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente_diagnosticar,resultado_paciente=resultado)
            # id_resultado =resultado_paciente.id
        else:
            y_pred = 'No tiene riesgo cardiovascular'

            # resultado = Resultado.objects.create(resultado=0)
            # resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente_diagnosticar,resultado_paciente=resultado)
            # id_resultado =resultado_paciente.id
        
        result = 0
        if(y_pred =='Si tiene riesgo cardiovascular'):
            result = 1
        imagen = Medico.objects.get(user__id=request.user.id)
        return render(request, 'generar-diagnostico.html', {'pacientes':pacientes_por_medico,'nombre_paciente':nombre_paciente,'apellido_paciente':apellido_paciente,'identidad_paciente':identidad_paciente,'result_riesgo' : y_pred,'paciente_id':user_id,'resultado_paciente':result,'medico_imagen':imagen,'paciente_individual':paciente_diagnosticar})
    return render(request, 'generar-diagnostico.html')

def aceptar_resultado_paciente(request, id,res):
    paciente = Paciente.objects.get(user__id=id)
    resultado = Resultado.objects.create(resultado=res)
    resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente,resultado_paciente=resultado)
    return http.HttpResponseRedirect('/medicos/generar-diagnostico')

def rechazar_resultado_paciente(request, id,res):
    if(res==1):
        res =0
    else:
        res =1
    paciente = Paciente.objects.get(user__id=id)
    resultado = Resultado.objects.create(resultado=res)
    resultado_paciente = ResultadoPaciente.objects.create(paciente=paciente,resultado_paciente=resultado)
    return http.HttpResponseRedirect('/medicos/generar-diagnostico')


    
def diagnostico_anonimo(request):
    imagen = Medico.objects.get(user__id=request.user.id)

    model = load('./savedModels/NeuralNetworkModel.joblib')
    if request.method == "POST": 

        edad = int(request.POST['edad'])
        sexo = int(request.POST['sexo'])
        peso = int(request.POST['peso'])
        talla = int(request.POST['talla'])
        diabetes = int(request.POST['diabetes'])
        sistolica = int(request.POST['presion_sistolica'])
        diastolica = int(request.POST['presion_diastolica'])
        colesterol = int(request.POST['colesterol_total'])
        hdl = float(request.POST['hdl'])
        ldl = float(request.POST['ldl'])
        triglicerios = int(request.POST['triglicerios'])
        tabaco = int(request.POST['tabaquismo'])
        antecedentes=int(request.POST['antecedentes'])
        print(edad, sexo, peso, talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes)
        y_pred = model.predict([[edad, sexo, peso, talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes]])
        if y_pred[0] == 1:
            y_pred = 'Si tiene riesgo cardiovascular'
        else:
            y_pred = 'No tiene riesgo cardiovascular'
        print(y_pred)
        paciente_anonimo = [edad,sexo,peso,talla,diabetes,sistolica,diastolica,colesterol,hdl,ldl,triglicerios,tabaco,antecedentes,y_pred]
        request.session['values_paciente_anonimo'] = paciente_anonimo

        return render(request,'diagnostico-anonimo.html',{'result_riesgo': y_pred,'medico_imagen':imagen})    
    return render(request,'diagnostico-anonimo.html',{'medico_imagen':imagen})

    
def agregar_pacientes(request):
    medico_imagen = Medico.objects.get(user__id=request.user.id)

    if request.method == "POST": 
        form = PacienteForm(request.POST,request.FILES) 
        if form.is_valid():  
            nombre_usuario = form.cleaned_data['nombre'][:3]+form.cleaned_data['apellido'][:3]+form.cleaned_data['identidad']
            pass_usuario = form.cleaned_data['apellido'][:2]+form.cleaned_data['nombre'][:2]+form.cleaned_data['identidad']
            nombre_paciente = form.cleaned_data['nombre']
            nombre_apellido = form.cleaned_data['apellido']
            user_paciente = User.objects.create_user(username=nombre_usuario,password=pass_usuario,is_paciente = True,nombre =nombre_paciente,apellido=nombre_apellido)
            form.instance.user = user_paciente

            form.save()
            medico_agregar = Medico.objects.get(user__id=request.user.id)
            paciente_agregar = Paciente.objects.get(user__id=user_paciente.id)
            medico_agregar.paciente.add(paciente_agregar)
            medico_imagen = Medico.objects.get(user__id=request.user.id)
            messages.success(request,'Guardar')
            # return http.HttpResponseRedirect('/')
            # return render(request,'agregar-pacientes.html', {'form':PacienteForm(request.GET)}) 
            return http.HttpResponseRedirect(request.path_info)
        else:
            print(form.errors)
    else:  
        form = PacienteForm()  
    return render(request,'agregar-pacientes.html', {'form':form,'medico_imagen':medico_imagen})

def listar_pacientes(request):
    print(request.user.id)
    # pacientes = Paciente.objects.filter(medicos__id=request.user.id)
    pacientes = Paciente.objects.all()
    imagen = Medico.objects.get(user__id=request.user.id)

    pacientes_por_medico = Medico.objects.get(user__id=request.user.id).paciente.all()
    return render(request,'listar-pacientes.html',{'pacientes':pacientes_por_medico,'medico_imagen':imagen})  

def actualizar_paciente_uno(request, id):  
    
    context ={}

    user = get_object_or_404(Paciente, user_id=id)
    form = PacienteForm(instance = user)
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
        messages.success(request,'Guardar')
        return http.HttpResponseRedirect('/medicos/listar-pacientes')

    context["form"] = form
    return render(request, "agregar-pacientes.html", context)


def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, user_id=id)
    paciente.delete()
    messages.success(request,'Eliminado')
    return http.HttpResponseRedirect('/medicos/listar-pacientes')

def editar_doctor(request):
    doctor = request.user.id
    context ={}

    user = get_object_or_404(Medico, user_id=doctor)
    form = MedicoForm(instance = user)
    medico_imagen = Medico.objects.get(user__id=request.user.id)

    if request.method == "POST":
        form = MedicoForm(request.POST, request.FILES, instance = user)

        if form.is_valid():
            form.save()
            messages.success(request,'Guardar')
            return http.HttpResponseRedirect(request.path_info)
        else:
            print(form.errors)
    context["form"] = form


    context["medico_imagen"] = medico_imagen
    return render(request, "editar_doctor.html", context)


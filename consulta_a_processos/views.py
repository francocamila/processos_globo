from django.shortcuts import render
from django.shortcuts import render
from .models import Processos
from django.http import HttpResponse
from django.shortcuts import render
from .utils import *
from django.template import loader
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import ProcessosForm
from djqscsv import render_to_csv_response
from djqscsv import write_csv
import csv
from csv import writer
import re
from datetime import datetime

#Lógica do site: Faz um request pra model e passa para um template. 

@csrf_exempt 
def cadastro_de_processos(request):

    #Filtrando os processos por data de atualização
    processos = Processos.objects.order_by('data_atualizacao')

    #Verifica se o botão "cadastrar" foi apertado. Então salva os inputs do request, bem como os resultados 
    #dos métodos que estão na utils.py e salva na Model. Também salva em um .csv e depois renderiza com o template.
    form = ProcessosForm(request.POST)
    if request.method == 'POST' and 'run_script' in request.POST:
        if form.is_valid():
            classe = request.POST.get("classe", None)
            numero = request.POST.get("numero", None)
            descricao = request.POST.get("descricao", None)
            emails = request.POST.get("emails", None)
            incidente_id = get_incidente_id(classe, numero)
            data_atualizacao = get_data_atualizacao(incidente_id)
            #passando a string resultante para queryset:
            data_atualizacao_queryset = datetime.strptime(data_atualizacao, "%d/%m/%Y").date()
            print(data_atualizacao_queryset)
            descricao_atualizacao = get_descricao_atualizacao(incidente_id)
            url = "http://portal.stf.jus.br/processos/detalhe.asp?incidente=" + incidente_id
            b4 = Processos(classe=str(classe), numero=str(numero), descricao=str(descricao), emails=str(emails), incidente_id=str(incidente_id), data_atualizacao = data_atualizacao_queryset, descricao_atualizacao = str(descricao_atualizacao), url = str(url))
            b4.save()
            fields=[classe, numero, incidente_id, descricao, data_atualizacao, descricao_atualizacao, emails, url]
            with open(r'resultados.csv', 'a', encoding = 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fields)             
        else:
            form = ProcessosForm()

    #if request.method == 'POST' and 'update_db' in request.POST:
        #primeiro todos os processos são filtrados pelo seu incidente_id
        #incidentes = Processos.objects.all().values('incidente_id')
        #inicia-se uma string vazia
        #incidente_string = ""
        #então pra cada incidente filtrado:
        #for incidente in incidentes:
            #acha-se apenas os números do queryset:
            #for ele in re.findall(r'\b\d+\b', str(incidente)):
                #transforma-se esse a lista resultante em string:
                #incidente_string += ele
                #atualiza-se a data e o andamento dos processos:                
                #data_atualizacao = get_data_atualizacao(incidente_string)
                #print(data_atualizacao)
                #descricao_atualizacao = get_descricao_atualizacao(incidente_string)
                #print(descricao_atualizacao)
                #então, pega-se cada incidente
                #update = Processos.objects.get(incidente_id=incidente_string)
                #atualiza-se os fields na database
                #update.data_atualizacao = data_atualizacao
                #update.descricao_atualizacao = descricao_atualizacao
                #fields são salvos na database
                #update.save()
                #incidente_string = ""
    qs = Processos.objects.all()
    with open('lista_de_processos.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'consulta_a_processos/cadastro_de_processos.html', {})       


    
def processos_list(request):
    posts = Processos.objects.filter().order_by('data_atualizacao')
    context_dict = {'processos': posts}
    return render(request, 'consulta_a_processos/processos_list.html', {'posts':posts})


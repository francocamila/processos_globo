import sys
sys.setrecursionlimit(1500)
from django.shortcuts import render, redirect
from .models import Processos
from django.http import HttpResponse
#importando tudo da utils, pois nela está os métodos de handling dos inputs
from .utils import *
from django.template import loader
#crud
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#timezone
from django.utils import timezone
#por causa do erro de csrf
from django.views.decorators.csrf import csrf_exempt
#forms
from .forms import ProcessosForm
#write csv
from djqscsv import render_to_csv_response
from djqscsv import write_csv
#para adicionar querysets em um csv
import csv
#para adicionar uma linha em resultados.csv
from csv import writer
#para procurar números em uma string
import re
#para converter string para datetime
from datetime import datetime
#authenticator:
from django.contrib.auth import authenticate, login, logout
#para retornar erro
from django.contrib import messages
#login required:
from django.contrib.auth.decorators import login_required
#logout


#Lógica do site: Faz um request pra model e passa para um template. 

@csrf_exempt 
@login_required(login_url='/')
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
            #data_atualizacao_queryset = datetime.strptime(data_atualizacao, "%d/%m/%Y").date()
            #print(data_atualizacao_queryset)
            descricao_atualizacao = get_descricao_atualizacao(incidente_id)
            url = "http://portal.stf.jus.br/processos/detalhe.asp?incidente=" + incidente_id
            b4 = Processos(classe=str(classe), numero=str(numero), descricao=str(descricao), emails=str(emails), incidente_id=str(incidente_id), data_atualizacao = str(data_atualizacao), descricao_atualizacao = str(descricao_atualizacao), url = str(url))
            b4.save()

            #escrevendo uma linha em resultados.csv
            fields=[classe, numero, incidente_id, descricao, data_atualizacao, descricao_atualizacao, emails, url]
            with open(r'resultados.csv', 'a', encoding = 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fields)             
        else:
            form = ProcessosForm()
    #salvando todos os querysets em um csv
    qs = Processos.objects.all()
    with open('lista_de_processos.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'consulta_a_processos/cadastro_de_processos.html')       

@login_required(login_url='/')
#views da página de listagem dos processos:    
def processos_list(request):
    posts = Processos.objects.filter().order_by('data_atualizacao')
    return render(request, 'consulta_a_processos/processos_list.html', {'posts':posts})

#views da página de login:
def login_user(request):
    return render(request, 'consulta_a_processos/login.html', {})

#views da autenticação:
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect ('/cadastro_de_processos/')
        else:
            messages.error(request, 'Usuário ou senha inválido.')
    return redirect('/')
    
@login_required(login_url='/')
def delete_process(request, process_id):
    process_id = int(process_id)
    try:
        process_sel = Processos.objects.get(id = process_id)
    except Processos.DoesNotExist:
        return redirect('/processos_list/')
    process_sel.delete()
    return redirect('/processos_list/')

def logout_request(request):
    logout(request)
    messages.info(request, "Usuário deslogado com sucesso!")
    return redirect("/")
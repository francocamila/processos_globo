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
# Create your views here.

@csrf_exempt 
def cadastro_de_processos(request):
    form = ProcessosForm()
    processos = Processos.objects.order_by('descricao')
    
    if request.method == 'POST' and 'run_script' in request.POST:
        form = ProcessosForm(request.POST)
        if form.is_valid():
            classe = request.POST.get("classe", None)
            numero = request.POST.get("numero", None)
            descricao = request.POST.get("descricao", None)
            emails = request.POST.get("emails", None)
            #incidente_id = get_incidente_id(classe, numero)
            #data_atualizacao = get_data_atualizacao(incidente_id)
            #descricao_atualizacao = get_descricao_atualizacao(incidente_id)
            #url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
            #essa função deve ser chamada de uma em uma hora:
            #atualizar_tabela_cadastro()
            save_table(classe, numero, descricao, emails)
            post = form.save(commit=False)
            post.save()
            
        else:
            form = ProcessosForm()
    
    #qs = Processos.objects.all()
    #with open('lista_de_processos.csv', 'wb') as csv_file:
    #    write_csv(qs, csv_file)
    return render(request, 'consulta_a_processos/cadastro_de_processos.html', {})        


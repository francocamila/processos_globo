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

            #essa função deve ser chamada de uma em uma hora:
            atualizar_tabela_cadastro()

            post = form.save(commit=False)
            post.save()
        else:
            form = ProcessosForm()
        #classe = request.POST.get("classe", None)
        #numero = request.POST.get("numero", None)
        #descricao = request.POST.get("descricao", None)
        #emails = request.POST.get("emails", None)
    # call function
    qs = Processos.objects.all()
    with open('lista_de_processos.csv', 'wb') as csv_file:
        write_csv(qs, csv_file)
    return render(request, 'consulta_a_processos/cadastro_de_processos.html', {})        

    def show_table(request):
    # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="resultados.csv"'

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
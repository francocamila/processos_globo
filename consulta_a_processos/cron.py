# -*- coding: utf-8 -*-
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
from .models import Processos


def atualizar_db():
    incidentes = Processos.objects.all().values('incidente_id')
        #inicia-se uma string vazia
    incidente_string = ""
        #então pra cada incidente filtrado:
    for incidente in incidentes:
            #acha-se apenas os números do queryset:
        for ele in re.findall(r'\b\d+\b', str(incidente)):
            #transforma-se esse a lista resultante em string:
            incidente_string += ele
                #atualiza-se a data e o andamento dos processos:                
            data_atualizacao = get_data_atualizacao(incidente_string)
            print(data_atualizacao)
            descricao_atualizacao = get_descricao_atualizacao(incidente_string)
            print(descricao_atualizacao)
                #então, pega-se cada incidente
            update = Processos.objects.get(incidente_id=incidente_string)
                #atualiza-se os fields na database
            update.data_atualizacao = data_atualizacao
            update.descricao_atualizacao = descricao_atualizacao
                #fields são salvos na database
            update.save()
            incidente_string = ""
    return
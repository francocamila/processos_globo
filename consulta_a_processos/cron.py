# -*- coding: utf-8 -*-
import os
import sys
import django
sys.path.append('/processos/consulta_a_processos/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'processos.settings'
from django.conf import settings

logger = get_task_logger(__name__)

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

def get_data_atualizacao(incidente_id):

    client = requests.session()
    url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
    response_andamento = client.get(url)
    print("- - - Get data atualização")
    html_page = response_andamento.content

    soup = BeautifulSoup(html_page, 'html.parser')

    andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
    return andamento_data

def get_descricao_atualizacao(incidente_id):

    client = requests.session()
    url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
    response_andamento = client.get(url)
    print("- - - Get descricao atualizacao")
    html_page = response_andamento.content

    soup = BeautifulSoup(html_page, 'html.parser')
    andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()    
    return andamento_nome 
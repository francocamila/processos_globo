from celery import shared_task
import re
from consulta_a_processos.models import *
from consulta_a_processos.utils import *

@shared_task
def hello():
    incidentes = Processos.objects.all().values('incidente_id')
        #inicia-se uma string vazia
    incidente_string = ""
        #então pra cada incidente filtrado:
    try:
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
    except Exception as e:
        print("Erro no update!")
        print(e)
    
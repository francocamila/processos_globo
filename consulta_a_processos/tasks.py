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
                current_model = Processos.objects.get(incidente_id=incidente_string)
    
                #atualiza-se a data e o andamento dos processos:                
                nova_data_atualizacao = get_data_atualizacao(incidente_string)
                print(nova_data_atualizacao)
                nova_descricao_atualizacao = get_descricao_atualizacao(incidente_string)
                print(nova_descricao_atualizacao)
                if (nova_data_atualizacao != str(current_model.data_atualizacao)) or (nova_descricao_atualizacao != str(current_model.descricao_atualizacao)):
                    print("hehe")
                #então, pega-se cada incidente
                    #update = Processos.objects.get(incidente_id=incidente_string)
                #atualiza-se os fields na database
                    current_model.data_atualizacao = nova_data_atualizacao
                    current_model.descricao_atualizacao = nova_descricao_atualizacao
                #fields são salvos na database
                    #try:
                    enviar_emails(str(current_model.classe), str(current_model.numero), str(current_model.descricao), str(current_model.descricao_atualizacao), str(current_model.data_atualizacao), incidente_string, str(current_model.emails))
                    #except Exception as e:
                        #print(e)
                    current_model.save()
                incidente_string = ""
    except Exception as e:
        print("Erro no update!")
        print(e)
    
# Bibliotecas para manipulacao de Dataframes (tabelas):
import pandas as pd
from pandas import DataFrame

# Bibliotecas para realizar scrapping de paginas HTML:
import requests
from bs4 import BeautifulSoup

# Importar o script de envio de e-mails:
import enviar_emails as ee

# Configuracao para criar log:
import logging
logging.basicConfig(filename='updates.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


# Metodo para consultar cada processo do arquivo "recultados.csv":
def atualizar_processos():
    # Leitura do arquivo com informacoes sobre os processos cadastrados:
    processos_df = pd.read_csv('resultados.csv')
    
    # Organiza a lista de processos com os processos mais recentemente atualizados primeiro:
    #processos_df['data_formatada'] = pd.to_datetime(processos_df.andamento_data)
    #processos_df = processos_df.sort_values(by='data_formatada', ascending=False)
    #processos_df = processos_df.drop('data_formatada', axis=1)
    #processos_df = processos_df.reset_index(drop=True)

    # Criacao de um novo Dataframe que conterá novas informações sobre os processos:
    resultados = []
    headings = ['classe', 'numero', 'incidente_id', 'descricao', 'andamento_data', 'andamento_nome', 'destinatarios', 'url']
    resultados.append(headings)

    # Criacao de um novo Dataframe que conterá apenas os processos atualizados:
    updates = []
    updates.append(headings)

    # Abrindo conexao com a internet:
    client = requests.session()

    try:
        # Para cada processo do arquivo CSV:
        for index, row in processos_df.iterrows():

            # Uma consulta ao portal do STF sera feita:
            url = 'http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=' + str(row.incidente_id)
            response_andamento = client.get(url)
            print('Incidente consultado: ' + str(index))
            html_page = response_andamento.content
            
            # Sera extraido do HTML da pagina as informacoes de data e nome da ultima atualizacao:
            soup = BeautifulSoup(html_page, 'html.parser')
            novo_andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
            novo_andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()

            # Se a ultima atualizacao for diferente da atualmente cadastrada, os novos dados serao armazenados:
            if (novo_andamento_data != row.andamento_data) or (novo_andamento_nome != row.andamento_nome):
                row['andamento_data'] = novo_andamento_data
                row['andamento_nome'] = novo_andamento_nome

                # Processos atualizados vao para a tabela de updates:
                updates.append(row)

            # Qualquer processo retorna para a tabela original de resultados:
            resultados.append(row)

    # Caso algum erro ocorra, ele sera salvo em "updates.log":
    except Exception as error:
        logger.error("Erro durante a consulta e montagem de tabelas: " + str(error))

    # Apos a consulta de todos os processos, os dados serao salvos num arquivo "resultados.csv":
    headers = resultados.pop(0)
    resultados_df = DataFrame(resultados, columns=headers)
    resultados_df.to_csv('resultados.csv',
                index = False,
                sep = ',',
                encoding = 'utf-8'
    )

    # A tabela com os processos atualizados tambem serao salvos num arquivo "updates.csv":
    headers = updates.pop(0)
    updates_df = DataFrame(updates, columns=headers)
    updates_df.to_csv('updates.csv',
                index = False,
                sep = ',',
                encoding = 'utf-8'
    )

    return 


# Inicio do script:
try:
    # Primeiro os processos serao consultados para saber se ha atualizacao:
    atualizar_processos()

    # Depois os emails serao enviados:
    ee.enviar_emails()

# Caso algum erro ocorra, o erro sera salvo em "updates.log":
except Exception as error:
    logger.error('Erro durante a atualizacao: ' + str(error))
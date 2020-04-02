import sys
from .models import *
import shutil
import os 
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_incidente_id(classe, numero):
    client = requests.session()
    processo_url = "http://portal.stf.jus.br/processos/listarProcessos.asp?classe=" + classe + "&numeroProcesso=" + numero
    response_processo = client.get(processo_url)
    
    redirect_url = response_processo.history[0].headers['location']
    incidente_id = redirect_url.split('=', 1)[1]

    return incidente_id

def atualizar_tabela_cadastro(classe, numero):
    arquivo_processos = "C:\\Users\\pedro\\Desktop\\processos_app\\lista_de_processos.csv"
    processos_df = pd.read_csv(arquivo_processos)

    datasets = []
    headings = ['Classe', 'Número', 'ID', 'Descrição', 'Data da Última Atualização', 'Descrição da Última Atualização', 'E-mail']
    datasets.append(headings)

    client = requests.session()

    try:
        for index, row in processos_df.iterrows():
            classe = row.classe
            numero = str(row.numero)
        
            incidente_id = get_incidente_id(classe, numero)
            print("- - - Get incidente number")
            url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
            response_andamento = client.get(url)
            print("- - - Get incidente")
            html_page = response_andamento.content
    
            soup = BeautifulSoup(html_page, 'html.parser')
    
            andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
            andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()
    
            dataset = [classe, numero, incidente_id, row.descricao, andamento_data, andamento_nome, row.emails]
            datasets.append(dataset)

    except Exception as e:
        print("Erro no scrapping!")
        print(e)

    headers = datasets.pop(0)
    export_df = DataFrame(datasets, columns=headers)
    filename = "C:\\Users\\pedro\\Desktop\\processos_app\\resultados.csv"
    export_df.to_csv(filename,
			    index = False,
			    sep = ',',
			    encoding = 'utf-8'
		    )
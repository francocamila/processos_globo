import sys
from .models import *
import shutil
import os 
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup
import csv   
from csv import writer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_table(classe, numero, descricao, emails):
    incidente_id = get_incidente_id(classe, numero)
    client = requests.session()
    url_find = "http://portal.stf.jus.br/processos/detalhe.asp?incidente=" + incidente_id
    url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id 
    response_andamento = client.get(url)
    print("- - - Get data atualização")
    html_page = response_andamento.content

    soup = BeautifulSoup(html_page, 'html.parser')

    andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
    andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()

    #with open('resultados.csv', 'a+', newline='') as write_obj:
    #            # Create a writer object from csv module
    #            csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
    #            csv_writer.writerow(classe, numero, incidente_id, descricao, andamento_data, andamento_nome, emails, url_find)
    #with open('resultados_novos.csv', 'a+', newline='') as write_obj:
                # Create a writer object from csv module
    #            csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
    #            csv_writer.writerow(classe, numero, incidente_id, descricao, andamento_data, andamento_nome, emails, url_find)
    fields=[classe, numero, incidente_id, descricao, andamento_data, andamento_nome, emails, url_find]
    with open(r'resultados.csv', 'a', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    with open(r'resultados_novos.csv', 'a', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    return

def get_incidente_id(classe, numero):
    client = requests.session()
    processo_url = "http://portal.stf.jus.br/processos/listarProcessos.asp?classe=" + classe + "&numeroProcesso=" + numero
    response_processo = client.get(processo_url)
    
    redirect_url = response_processo.history[0].headers['location']
    incidente_id = redirect_url.split('=', 1)[1]

    return incidente_id


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

def atualizar_tabela_cadastro():
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


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
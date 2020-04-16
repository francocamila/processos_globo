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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Aqui tem todos os métodos do site.

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

def enviar_emails(classe, numero, descricao, descricao_atualizacao, data_atualizacao, incidente_id, email):
    # Conexao com o servidor do Gmail, utilizando login e senha:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('processosglobobsa@gmail.com', 'TVG@bsa#processos')

        # Informacoes de remetentes e destinatarios:
    sender = 'processosglobobsa@gmail.com'
        #to_addresses = 'mvjunior@g.globo, fernanda.vivas@g.globo, rosanne.dagostino@g.globo'
        #cc_addresses = 'camila.franco@g.globo, cassio.fabius@g.globo'
        #bcc_addresses = 'adonias.melo@g.globo, esousa@g.globo, lgcarvalho@g.globo, matheus.moreira@g.globo'
        #recipients_addresses = to_addresses.split(",") + cc_addresses.split(",") + bcc_addresses.split(",")
    to_addresses = email
    recipients_addresses = to_addresses
        # Assunto do e-mail:
    subject = 'Atualização de processos do STF: ' + str(descricao)

        # Corpo do e-mail:
    message = '<html><body><p>Olá!</p><p>O seguinte processo foi atualizado: ' + str(classe) + ' ' + str(numero) + \
                '</p><p>Descrição da atualização: ' + str(descricao_atualizacao) + ' em: ' + str(data_atualizacao) + \
                '.</p><p>Para acompanhar o processo, <a href="http://portal.stf.jus.br/processos/detalhe.asp?incidente=' + str(incidente_id) + '">clique aqui</a>.</p>' + \
                '<p>Atenciosamente, Tecnologia Brasília.</p></body></html>' 
        
        # Montagem do e-mail:
    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = to_addresses
    #msg['Cc'] = cc_addresses
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html', 'utf-8'))

    text = msg.as_string()

        # Envio do e-mail para os destinatarios:
    server.sendmail(sender, recipients_addresses, text)

    # Finalizacao da conexao com o Gmail apos o envio de todos os e-mails:
    server.quit()

    # Limpa o arquivo "updates.csv" para a proxima consulta:

    return

import smtplib
import email.message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from pandas import DataFrame
import requests
from bs4 import BeautifulSoup


def atualizar_tabela_cadastro():
    arquivo_processos = "resultados.csv"
    processos_df = pd.read_csv(arquivo_processos)

    datasets = []
    headings = ['Classe', 'Numero', 'ID', 'Topico', 'Data_da_Ultima_Atualizacao', 'Descricao_da_Ultima_Atualizacao', 'Email', 'URL']
    datasets.append(headings)

    client = requests.session()

    try:
        for index, row in processos_df.iterrows():
            classe = row.Classe
            numero = str(row.Numero)
            descricao = row.Topico
            incidente_id = str(row.ID)
            print("- - - Get incidente number")
            url = "http://portal.stf.jus.br/processos/abaAndamentos.asp?incidente=" + incidente_id
            response_andamento = client.get(url)
            print("- - - Get incidente")
            html_page = response_andamento.content
    
            soup = BeautifulSoup(html_page, 'html.parser')
    
            andamento_data = soup.find("div", {"class": "andamento-data"}).get_text()
            andamento_nome = soup.find("h5", {"class": "andamento-nome"}).get_text()
    
            dataset = [classe, numero, incidente_id, descricao, andamento_data, andamento_nome, row.Email, row.URL]
            datasets.append(dataset)

    except Exception as e:
        print("Erro no scrapping!")
        print(e)

    headers = datasets.pop(0)
    export_df = DataFrame(datasets, columns=headers)
    filename = "resultados_novos.csv"
    export_df.to_csv(filename,
			    index = False,
			    sep = ',',
			    encoding = 'utf-8'
		    )
    return 

def send_email(email, classe, numero, descricao, data, descricao_at, url):
    sender = 'processosglobobsa@gmail.com'
    password = 'TVG@bsa#processos'
    send_to_email = email
    cc1 = 'camila.franco@g.globo'
    cc2 = 'adonias.melo@g.globo'
    cc3 = 'esousa@g.globo'
    cc4 = 'cassio.fabius@g.globo'
    cc5= 'matheus.moreira@g.globo'
    subject = 'Atualização de processos do STF: ' + str(descricao) # The subject line
    message = 'Olá! \n\n\n Os seguinte processo foi atualizado: ' + str(classe) + str(numero) + '\n\nDescrição da atualização: ' + str(descricao_at) + ' em: ' + str(data) + '. \n\n Para acompanhar o processo, clique aqui:' + str(url)
    
    msg = MIMEMultipart()
    #msg = MIMEText(message ,'html')
    msg['From'] = sender
    msg['To'] = send_to_email
    msg['Subject'] = subject

 # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(sender, send_to_email, text)
    server.sendmail(sender, cc1, text)
    server.sendmail(sender, cc2, text)
    server.sendmail(sender, cc3, text)
    server.sendmail(sender, cc4, text)
    server.sendmail(sender, cc5, text)
    server.quit()
    return
    

atualizar_tabela_cadastro()
with open('resultados.csv', 'r') as t1, open('resultados_novos.csv', 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

datasets = []
headings = ['Classe', 'Numero', 'ID', 'Topico', 'Data_da_Ultima_Atualizacao', 'Descricao_da_Ultima_Atualizacao', 'Email']
datasets.append(headings)
headers = datasets.pop(0)
export_df = DataFrame(datasets, columns=headers)
filename = "update.csv"

with open('update.csv', 'w') as outFile:
    outFile.write("Classe,Numero,ID,Topico,Data_da_Ultima_Atualizacao,Descricao_da_Ultima_Atualizacao,Email,URL")
    outFile.write("\n")
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)
            #update = "lalala"
        #else:
            #update="not_true"



arquivo_update = "update.csv"
updates = pd.read_csv(arquivo_update)

try:
    for index, row in updates.iterrows():
        email = row.Email
        classe = row.Classe
        numero = row.Numero
        descricao = row.Topico
        data = row.Data_da_Ultima_Atualizacao
        descricao_at = row.Descricao_da_Ultima_Atualizacao
        url = row.URL
        send_email(email, classe, numero, descricao, data, descricao_at, url)
except Exception as e:
    print("Sem mudanças!")
    print(e)
#if update == "lalala":
    #send_email()
filename = "update.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

with open('resultados.csv', 'w') as outFile:
    for line in filetwo:
            outFile.write(line)
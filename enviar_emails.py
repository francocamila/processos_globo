# Bibliotecas para manipulacao de Dataframes (tabelas):
import pandas as pd

# Bibliotecas para montagem e envio de e-mails:
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Metodo para enviar emails com atualizacoes de processos:
def enviar_emails():
    # Conexao com o servidor do Gmail, utilizando login e senha:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('processosglobobsa@gmail.com', 'TVG@bsa#processos')

    # Leitura do arquivo CSV com processos atualizados:
    updates = pd.read_csv('updates.csv')

    # Para cada processo, enviar um email:
    for index, row in updates.iterrows():

        # Informacoes de remetentes e destinatarios:
        sender = 'processosglobobsa@gmail.com'
        to_addresses = 'mvjunior@g.globo, fernanda.vivas@g.globo, rosanne.dagostino@g.globo'
        cc_addresses = 'camila.franco@g.globo, cassio.fabius@g.globo'
        bcc_addresses = 'adonias.melo@g.globo, esousa@g.globo, lgcarvalho@g.globo, matheus.moreira@g.globo'
        recipients_addresses = to_addresses.split(",") + cc_addresses.split(",") + bcc_addresses.split(",")

        # Assunto do e-mail:
        subject = 'Atualização de processos do STF: ' + str(row.descricao)

        # Corpo do e-mail:
        message = '<html><body><p>Olá!</p><p>O seguinte processo foi atualizado: ' + str(row.classe) + ' ' + str(row.numero) + \
                    '</p><p>Descrição da atualização: ' + str(row.andamento_nome) + ' em: ' + str(row.andamento_data) + \
                    '.</p><p>Para acompanhar o processo, <a href="http://portal.stf.jus.br/processos/detalhe.asp?incidente=' + str(row.incidente_id) + '">clique aqui</a>.</p>' + \
                    '<p>Atenciosamente, Tecnologia Brasília.</p></body></html>' 
        
        # Montagem do e-mail:
        msg = MIMEMultipart()

        msg['From'] = sender
        msg['To'] = to_addresses
        msg['Cc'] = cc_addresses
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'html', 'utf-8'))

        text = msg.as_string()

        # Envio do e-mail para os destinatarios:
        server.sendmail(sender, recipients_addresses, text)

    # Finalizacao da conexao com o Gmail apos o envio de todos os e-mails:
    server.quit()

    # Limpa o arquivo "updates.csv" para a proxima consulta:
    f = open('updates.csv', "w+")
    f.close()

    return

# Descomente a linha abaixo caso queira testar apenas este codigo:
#enviar_emails()
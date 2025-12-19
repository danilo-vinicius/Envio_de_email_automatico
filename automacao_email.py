import smtplib
import schedule
import time
import pytz
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os

#SMTP_SERVER = "smtp.gmail.com"
#SMTP_PORT = 587
#EMAIL_REMETENTE = "correio.empresa@gmail.com"
#SENHA_APP = "oucjistxahlgsbxq"

SMTP_SERVER = "correio.empresa.com.br"
SMTP_PORT = 587
EMAIL_REMETENTE = "naoresponda@empresa.com.br"
SENHA_EMAIL = "Naorespon145@87#_p"

# Destinatários
DESTINATARIOS = ["destinatario1@empresa.com.br", "destinatario2@empresa.com.br", "destinatario3@empresa.com.br", "destinatario4@empresa.com.br"]

# Define fuso horário de Brasília
fuso_brasilia = pytz.timezone("America/Sao_Paulo")
# Caminho do arquivo a ser anexado

CAMINHO_ARQUIVO = r"Z:\local1\Nome\destino1\Arquivo.zip"

# FUNÇÃO DE ENVIO
# ==========================
def enviar_email():
    from datetime import datetime, timedelta
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import os

    # Fuso horário de Brasília
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(fuso_brasilia)
    semana_passada = hoje - timedelta(days=5)

    # Corpo do e-mail
    corpo_email = f"""
Prezados,

Segue em anexo o relatório referente ao período de {semana_passada.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}.

O documento contém o resumo das atividades realizadas, pendências em aberto e registros das manutenções efetuadas durante o período.

Qualquer dúvida ou informação adicional, estou à disposição.

Atenciosamente,
Equipe de Suporte
Empresa
"""

    # Assunto do e-mail
    assunto = f"Relatório Semanal – {hoje.strftime('%d/%m/%Y')}"

    try:
        # Cria a estrutura do e-mail
        mensagem = MIMEMultipart()
        mensagem["From"] = EMAIL_REMETENTE
        mensagem["To"] = ", ".join(DESTINATARIOS)
        mensagem["Subject"] = assunto

        # Corpo do e-mail
        mensagem.attach(MIMEText(corpo_email, "plain"))

        # Anexo
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, "rb") as arquivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(arquivo.read())
                encoders.encode_base64(parte)
                parte.add_header(
                    "Content-Disposition",
                    'attachment; filename="Controle_Semanal_Ciplan.zip"'
                )
                mensagem.attach(parte)
        else:
            print(f"❌ Arquivo não encontrado em: {CAMINHO_ARQUIVO}")
            return

        # Envio do e-mail
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()  # ativa o protocolo TLS
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.send_message(mensagem)
        servidor.quit()
        print(f"[{datetime.now()}] ✅ E-mail enviado com sucesso!")

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erro ao enviar e-mail: {e}")

# Codigo de Lembrete
def enviar_lembrete():
    tz = pytz.timezone("America/Sao_Paulo")
    hoje = datetime.now(tz)
    assunto = f"⏰ Lembrete: Preparar arquivo para envio – {hoje.strftime('%d/%m/%Y')}"
    corpo = """
Bom dia!

Lembrete: preparar o arquivo ZIP de Ordens de Serviço para envio automático hoje às 17h00.

Verifique se o relatório semanal foi atualizado na pasta:

Z:\local1\Nome\destino1\Arquivo.zip

Atenciosamente,
Equipe de Segurança Eletrônica
Brasfort
"""
    enviar_email(assunto, corpo)

# AGENDAMENTO
# ==========================

# define o dia e a hora
dia_da_semana = "friday"
hora = "17:00"

# Dicionário para traduzir para português
dias_traduzidos = {
    "monday": "segunda-feira",
    "tuesday": "terça-feira",
    "wednesday": "quarta-feira",
    "thursday": "quinta-feira",
    "friday": "sexta-feira",
    "saturday": "sábado",
    "sunday": "domingo"
}

# Configura o agendamento dinâmico
schedule.every().friday.at("09:00").do(enviar_lembrete) 
getattr(schedule.every(), dia_da_semana).at(hora).do(enviar_email)

# Mensagem amigável com tradução
print(f"⏰ Automação iniciada. O lembrete será enviado toda {dias_traduzidos[dia_da_semana]} às 09:00.")
print(f"⏰ Automação iniciada. O e-mail será enviado toda {dias_traduzidos[dia_da_semana]} às {hora}.")

# Loop de execução contínua
while True:
    schedule.run_pending()
    time.sleep(60)



import smtplib
import schedule
import time
import pytz
import os
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta

# ==========================================
# CONFIGURAÇÕES (Carregadas via Variáveis de Ambiente ou Placeholders)
# ==========================================

# Configurações do Servidor SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.seu-servidor.com.br")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_REMETENTE = os.getenv("EMAIL_USER", "seu_email@empresa.com.br")
SENHA_EMAIL = os.getenv("EMAIL_PASSWORD", "sua_senha_aqui")

# Destinatários (Pode ser uma string separada por vírgulas nas variáveis de ambiente)
destinatarios_str = os.getenv("EMAIL_DESTINATARIOS", "gestor@empresa.com.br,suporte@empresa.com.br")
DESTINATARIOS = [email.strip() for email in destinatarios_str.split(",")]

# Configurações de Arquivo e Fuso
CAMINHO_ARQUIVO = os.getenv("PATH_ARQUIVO", r"C:\Caminho\Para\Arquivo.zip")
FUSO_BRASILIA = pytz.timezone("America/Sao_Paulo")

# ==========================================
# FUNÇÕES DE ENVIO
# ==========================================

def enviar_email(assunto=None, corpo=None, anexo=None):
    """
    Função genérica para envio de e-mail com anexo opcional.
    """
    try:
        # Define valores padrão se não forem passados
        hoje = datetime.now(FUSO_BRASILIA)
        
        if not assunto:
            assunto = f"Relatório Semanal – {hoje.strftime('%d/%m/%Y')}"
        
        if not corpo:
            semana_passada = hoje - timedelta(days=5)
            corpo = f"""
            Prezados,

            Segue em anexo o relatório referente ao período de {semana_passada.strftime('%d/%m/%Y')} a {hoje.strftime('%d/%m/%Y')}.
            O documento contém o resumo das atividades realizadas e pendências.

            Atenciosamente,
            Equipe de Suporte
            """

        # Cria a estrutura do e-mail
        mensagem = MIMEMultipart()
        mensagem["From"] = EMAIL_REMETENTE
        mensagem["To"] = ", ".join(DESTINATARIOS)
        mensagem["Subject"] = assunto

        # Adiciona o corpo do texto
        mensagem.attach(MIMEText(corpo, "plain"))

        # Adiciona Anexo (se houver caminho informado e o arquivo existir)
        if anexo and os.path.exists(anexo):
            with open(anexo, "rb") as arquivo:
                parte = MIMEBase("application", "octet-stream")
                parte.set_payload(arquivo.read())
                encoders.encode_base64(parte)
                parte.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{os.path.basename(anexo)}"'
                )
                mensagem.attach(parte)
        elif anexo:
            print(f"⚠️ Aviso: Arquivo não encontrado em: {anexo}")

        # Conexão e Envio
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls() 
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        servidor.send_message(mensagem)
        servidor.quit()
        
        print(f"[{datetime.now()}] ✅ E-mail enviado com sucesso: '{assunto}'")

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erro ao enviar e-mail: {e}")

def job_envio_relatorio():
    """Função wrapper para ser chamada pelo agendador (Schedule)"""
    print("Iniciando rotina de envio de relatório...")
    enviar_email(anexo=CAMINHO_ARQUIVO)

def job_envio_lembrete():
    """Envia lembrete para a equipe preparar os arquivos"""
    hoje = datetime.now(FUSO_BRASILIA)
    assunto = f"⏰ Lembrete: Preparar arquivo para envio – {hoje.strftime('%d/%m/%Y')}"
    corpo = f"""
    Bom dia!

    Lembrete: preparar o arquivo ZIP de Ordens de Serviço para envio automático hoje às 17h00.
    Verifique se o relatório foi salvo corretamente no diretório de rede.

    Atenciosamente,
    Equipe de Segurança Eletrônica
    """
    enviar_email(assunto=assunto, corpo=corpo)

# ==========================================
# AGENDAMENTO
# ==========================================

# Configura o agendamento
# Lembrete às 09:00 toda Sexta
schedule.every().friday.at("09:00").do(job_envio_lembrete)

# Relatório às 17:00 toda Sexta
schedule.every().friday.at("17:00").do(job_envio_relatorio)

print("🤖 Bot de Automação de E-mails Iniciado...")
print("📅 Agendamento: Sextas-feiras às 09:00 (Lembrete) e 17:00 (Relatório).")

# Loop infinito
while True:
    schedule.run_pending()
    time.sleep(60)

# Automação de Relatórios Corporativos via E-mail 📧

Este projeto consiste em um script Python desenvolvido para automatizar a rotina de envio de relatórios semanais e lembretes operacionais para a equipe de Segurança Eletrônica.

O script elimina a necessidade de envio manual, garantindo que os stakeholders recebam os dados consolidados sempre no mesmo horário, além de notificar a equipe técnica previamente para a preparação dos arquivos.

## ⚙️ Funcionalidades

* **Envio Automático:** Dispara e-mails com anexos (.zip) automaticamente.
* **Agendamento Inteligente:** Utiliza a biblioteca `schedule` para rodar tarefas em dias e horários específicos (toda sexta-feira).
* **Log de Execução:** Feedback visual no console sobre o status do envio.
* **Segurança:** Credenciais e configurações sensíveis separadas do código fonte (Environment Variables).

## 🛠 Tecnologias Utilizadas

* **Python 3.x**
* **Smtplib:** Protocolo de envio de e-mails.
* **Schedule:** Agendamento de tarefas (Cron jobs).
* **Pytz:** Gerenciamento de fuso horário (Brasília).
* **OS/Dotenv:** Gerenciamento de variáveis de ambiente.

## 🚀 Como Configurar

Para rodar este projeto, é necessário configurar as variáveis de ambiente com as credenciais do seu servidor de e-mail corporativo ou Gmail.

```python
# Exemplo de configuração (.env)
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
EMAIL_USER="seu_email@dominio.com"
EMAIL_PASSWORD="sua_senha_de_app"
PATH_ARQUIVO="Z:/Rede/Relatorios/arquivo.zip"
```

## 📋 Estrutura do Agendamento

1. 09:00 (Sexta-feira): Envia um e-mail de lembrete para a equipe técnica preparar o arquivo na rede.

2. 17:00 (Sexta-feira): O script busca o arquivo no diretório especificado e o envia em anexo para a lista de gestores.

Desenvolvido por Danilo Vinícius

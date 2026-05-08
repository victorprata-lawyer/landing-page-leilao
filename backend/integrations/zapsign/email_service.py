import os
import smtplib
import ssl
from email.mime.text import MIMEText

def send_initial_layer_email(codigo: str, to_email: str):
    """
    Envia e-mail da camada inicial ao concluir assinatura no ZapSign.
    """
    # Validação de variáveis de ambiente
    required_envs = {
        'SMTP_HOST': os.getenv('SMTP_HOST'),
        'SMTP_PORT': os.getenv('SMTP_PORT'),
        'SMTP_USER': os.getenv('SMTP_USER'),
        'SMTP_PASSWORD': os.getenv('SMTP_PASSWORD'),
        'EMAIL_FROM': os.getenv('EMAIL_FROM'),
    }
    for name, value in required_envs.items():
        if not value:
            raise ValueError(f"Variável de ambiente '{name}' é obrigatória e não foi definida.")

    smtp_host = required_envs['SMTP_HOST']
    smtp_port = int(required_envs['SMTP_PORT'])
    smtp_user = required_envs['SMTP_USER']
    smtp_password = required_envs['SMTP_PASSWORD']
    email_from = required_envs['EMAIL_FROM']

    # Conteúdo do e-mail
    subject = f'[{codigo}] | Fluxo Protegido Formalizado | Camada Inicial'
    body = f"""
Olá,

A camada inicial do fluxo protegido foi concluída com sucesso!

- Confidencialidade formalizada
- Fluxo protegido ativado
- Documentação inicial controlada
- Resumo jurídico do ativo
- Leitura preliminar de risco
- Sequência formal até o Data Room

Código do Ativo: {codigo}

Atenciosamente,
Equipe
    """

    # Criação e envio do e-mail com TLS
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

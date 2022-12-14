from email.message import EmailMessage
import ssl
import smtplib

email_sender = "refapetccadm@gmail.com"
email_password="fdrbkclugfamrdvv"
email_receiver="italonunespereira@outlook.com"
senha = "fdrbkclugfamrdvv"

def envioEmail(nome,email,assunto,mensagem):
    try:
        subject=str(assunto)
        body='''
        {} responsavel pelo email {} enviou a seguinte mensagem:
        {}
        '''.format(nome,email,mensagem)
        em = EmailMessage()
        em['From']=email_sender
        em['To']=email_receiver
        em['Subject']=subject
        em.set_content(body)

        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
            envioEmailCliente(email)
            return True
    except:
        return False

def envioEmailCliente(email):
    try:
        subject="retorno automatico"
        body='''
        obrigado por enviar um email, vamos retornar assim que posivel 
        equipe ReFaPe
        '''
        em = EmailMessage()
        em['From']=email_sender
        em['To']=email
        em['Subject']=subject
        em.set_content(body)

        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
            return True
    except:
        return False

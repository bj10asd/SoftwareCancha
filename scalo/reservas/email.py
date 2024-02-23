from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.shortcuts import render
from scalo.settings import base
#Envia mail al cliente
def send_cliente_email(datos_send_mail):


    #template = get_template('mails/cliente.html')
    template = get_template('mails/cliente_nuevo.html')

    content = template.render(datos_send_mail)

    email = EmailMessage(
        'Asunto del correo',
        content,
        #settings.EMAIL_HOST_USER, #Remitente
        base.EMAIL_HOST_USER, #Remitente
        [datos_send_mail['mail']]) #Destinatario
    email.content_subtype = 'html'
    email.send()


#Evnia mail al propitario
def send_predio_email(datos_send_mail):


    #template = get_template('mails/predio.html')

    #content = template.render(datos_send_mail)

    email = EmailMessage(
        'Asunto del correo',
        #content,
        #settings.EMAIL_HOST_USER, #Remitente
        base.EMAIL_HOST_USER, #Remitente
        [datos_send_mail['predio_email']]) #Destinatario
    email.content_subtype = 'html'
    email.send()
    
    
def send_mail_verificar(request):
    return render(request,'mails/verificar_usuario.html',{})#,{'canchas':cancha})

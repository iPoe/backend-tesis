from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say, Play
from django.conf import settings
from email.mime.text import MIMEText 
import smtplib
import requests


""" Configurar toda la conexión con la API paga de Twilio """
def load_twilio_config():
    twilio_account_sid = settings.TID
    twilio_auth_token = settings.T_AUTH_TOKEN
    twilio_number = settings.TNUMBER
    twilio_number_whatsapp = settings.TNUMBER
    return twilio_number, twilio_account_sid, twilio_auth_token, twilio_number_whatsapp


def load_email_config():
    email_smtp_dir = settings.SMTP_HOSTNAME
    email_email = settings.EMAIL_USER
    email_password = settings.EMAIL_PASSWORD
    return email_email, email_password, email_smtp_dir


""" Clase que permite enviar un mensaje de texto || send_message(mensaje, celular)"""
class SMS:
    def __init__(self):
        (twilio_number, twilio_account_sid, twilio_auth_token, twilio_number_whatsapp) = load_twilio_config()
        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

    def send_message(self, body, to, idMensaje):
        self.twilio_client.messages.create(
            body=body,
            to=to,
            from_=self.twilio_number,
            status_callback='https://coffee-cuscus-4020.twil.io/status-callback-sms?idMensaje='+idMensaje
        )


""" Clase que permite realizar una llamada telefónica || voice_call(text, URLmp3, celular) """
class VoiceCall:
    def __init__(self):
        (twilio_number, twilio_account_sid, twilio_auth_token, twilio_number_whatsapp) = load_twilio_config()
        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
    
    def voice_call(self, voiceCall, urlMP3, to, idLlamada):
        response = VoiceResponse()
        say = Say(voiceCall, voice='Polly.Lupe-Neural')
        response.append(say)
        if(urlMP3 != ''):
            response.play(urlMP3)
        call = self.twilio_client.calls.create(
            twiml = response,
            to=to,
            from_=self.twilio_number,
            status_callback='https://coffee-cuscus-4020.twil.io/status-callback-voice?idLlamada='+idLlamada,
            status_callback_method='POST',
            timeout=30,
        )
        print(call.sid)


""" Clase que permite enviar un mensaje por WhatsApp || send_message(mensaje, celular) || send_media(mensaje, celular, urlPNG)"""
class WhatsApp:
    def __init__(self):
        (twilio_number, twilio_account_sid, twilio_auth_token, twilio_number_whatsapp) = load_twilio_config()
        self.twilio_number_whatsapp = twilio_number_whatsapp
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

    def send_message(self, body, to,idLlamada):
        message_whatsapp = self.twilio_client.messages.create(
            body=body,
            to='whatsapp:'+to,
            from_='whatsapp:'+self.twilio_number_whatsapp,
        )
        print(message_whatsapp.sid)

    def send_media(self, body, to, image):
        message_whatsapp = self.twilio_client.messages.create(
            body=body,
            to='whatsapp:'+to,
            from_='whatsapp:'+self.twilio_number_whatsapp,
            media_url=[image]
        )
        print(message_whatsapp.sid)


""" Enviar un Email, aunque aun no funciona bien || send_email(mensaje, emailDestino, asunto) """
class Email:
    def __init__(self):
        print('Initializing Email client')
        (
            email_email,
            email_password,
            email_smtp_dir,
        ) = load_email_config()
        self.email_email = email_email
        self.server = smtplib.SMTP(email_smtp_dir)
        self.server.starttls()
        self.server.login(email_email, email_password)
        print('Email initialized')

    def send_email(self, body, to, subject):
        message_email = MIMEText(body)
        message_email['From'] = self.email_email
        message_email['To'] = ", ".join(to)
        message_email['Subject'] = subject
        text = message_email.as_string()
      
        self.server.sendmail(
            self.email_email,
            to, text
        )
        self.server.close()


def main():
    numeroPaula = '+573006124086'
    numeroWilliam = '+573022118294'
    numeroJP = '+573014210167'
    numeroFijo = '+5722262430'
    numeroLeo = '+573177947129'

    """ clientSMS = SMS()
    clientSMS.send_message('¡Hola Buenos días! Paula Recuerda nuestra reunión de las 10:00am del día 23 de diciembre, Atentamente: Software de Salud Pública', numeroWilliam, 'William') """
    """ 
    for admin in administrators:
        clientSMS.send_message(message_to_send, admin['phone_number'])
    """

    """
    clientWhatsApp = WhatsApp()
    clientWhatsApp.send_media('¡Esto es una super prueba desde Salud Pública para el mundo!', '+573022118294', 'https://demo.twilio.com/owl.png')
    """
    
    #clientEmail = Email()
    
    
    clientVoice = VoiceCall()
    mensajeVoz = '¡Hola! Te llamamos desde Salud Pública, queremos darte la bienvenida a las nueva era digital de las llamadas automáticas, es un placer para mi hablarte, deseo que pronto nos conozcamos, ¡Muchas gracias! Y te deseo una Feliz Navidad y Próspero año nuevo, ¡Hasta luego y lindo día!'
    mp3 = 'https://dl.dropboxusercontent.com/s/3teh8x28x3kre75/Prueba-1.mp3'
    mp3_2 = ''
    clientVoice.voice_call(mensajeVoz, mp3, numeroJP, 'William') #Telefono Fijo
    #clientVoice.voice_call(mensajeVoz, mp3_2, numeroFijo, 'William') #Celular



from ast import Try
from curses.ascii import EM
import datetime
import pytz
import json
from django.conf import settings
import smtplib
from email.mime.text import MIMEText

from django.db import transaction
from celery import shared_task
from datetime import date
from .models import Campania,estado_campania,mediosxcampania,Medio,contactosxcampa,resultadosxcampania,	Tipo_resultado

from django_celery_beat.models import IntervalSchedule, PeriodicTask,CrontabSchedule
from .twilioAPI import VoiceCall,SMS,Email,WhatsApp

clientSMS = SMS()
clientVoice = VoiceCall()
clientWhatsapp = WhatsApp()
#whatsapp_Template = 'Hola te escribimos de parte de la Red de Salud Ladera, el dia de hoy tenemos información muy importante para ti, si deseas saber mas por favor responde a este mensaje.'
whatsapp_Template = "¡Hola! Te escribimos para hacerte parte de una prueba de servicios de tamizaje con la Red de Salud Ladera. Te solicitamos responder el número de acuerdo a tu preferencia.\n  1. SI deseo participar en la prueba\n2. NO deseo participar en la prueba"

def crearTareaCampaña(campId,hora,minute,mId,tel=""):
    cam = Campania.objects.get(pk=campId)
    m = Medio.objects.get(pk = mId)
    name = "Task" + str(m.id)+str(hora)+str(minute)

    idTask = []
    if m.tipo_medio.descripcion == 4:            
        schedule = customSchedule(hora,minute)
        sms_camp= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='enviar_sms',
            args=json.dumps([campId,mId]),
            start_time=datetime.datetime.now()
        )
        idTask.append(sms_camp.id)
    elif m.tipo_medio.descripcion == 2:
        tel = 1
        schedule = customSchedule(hora,minute)
        llamadaTel= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='llamadas',
            args=json.dumps([campId,mId,tel]),
            start_time=datetime.datetime.now()
        )
        idTask.append(llamadaTel.id)
    elif m.tipo_medio.descripcion == 1:
        schedule = customSchedule(hora,minute)
        llamadaCel= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='llamadas',
            args=json.dumps([campId,mId]),
            start_time=datetime.datetime.now()
        )
        idTask.append(llamadaCel.id)
    elif m.tipo_medio.descripcion == 3:
        schedule = customSchedule(hora,minute)
        envioCorreos= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='correos',
            args=json.dumps([campId,mId]),
            start_time=datetime.datetime.now()
        )
        idTask.append(envioCorreos.id)
    elif m.tipo_medio.descripcion == 5:
        schedule = customSchedule(hora,minute)
        enviarWp= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='enviar_wp',
            args=json.dumps([campId,mId]),
            start_time=datetime.datetime.now()
        )
        idTask.append(enviarWp.id)
    else:
        pass

    cam.tasksIds.append(idTask)
    cam.save()
    
def llamar_usuarias(ID,mId,tel=''):
    cons = contactosxcampa.objects.filter(campania = ID)
    m = Medio.objects.get(pk=mId)
    fechaActual = date.today()
    numerosUsuarias = ["+57"+obj.contacto.celular for obj in cons]
    if tel == 1:
        numerosUsuarias = ["+57"+obj.contacto.telefono for obj in cons]
    matchUrlAudio = True if "http" in m.sms_mensaje else False
    mensajeVoz, urlAUdio = m.sms_mensaje if not matchUrlAudio else '', m.sms_mensaje+".mp3" if matchUrlAudio else ''
    camp = Campania.objects.get(pk = ID)
    cant = len(numerosUsuarias)
    for n in range(cant):
        res = resultadosxcampania(contacto_cc=cons[n].contacto,campania_id=camp,medio_id=m,fecha=fechaActual)
        res.save()
        clientVoice.voice_call(mensajeVoz, urlAUdio, numerosUsuarias[n], str(res.id))

def envMensajeUsuarias(ID,mId):
    cons = contactosxcampa.objects.filter(campania = ID)
    m,fechaActual = Medio.objects.get(pk=mId),date.today()
    txt = m.sms_mensaje
    numerosUsuarias = ["+57"+obj.contacto.celular for obj in cons]    
    camp = Campania.objects.get(pk = ID)
    cant = len(numerosUsuarias)
    for n in range(cant):
        res = resultadosxcampania(contacto_cc=cons[n].contacto,campania_id=camp,medio_id=m,fecha=fechaActual)
        res.save()
        clientSMS.send_message(txt, numerosUsuarias[n], str(res.id))

def enviar_correos(ID,mId):
    usuariasCamp = contactosxcampa.objects.filter(campania = ID)
    correosUsuarios = [ usuaria.contacto.email for usuaria in usuariasCamp]
    m = Medio.objects.get(pk=mId)
    camp = Campania.objects.get(pk = ID)
    usuarios_campaña = contactosxcampa.objects.filter(campania = ID)
    tipoRes = Tipo_resultado.objects.get( descripcion = "si" )
    for usuario in usuarios_campaña:
        res = resultadosxcampania(contacto_cc = usuario.contacto, campania_id = camp, medio_id = m, fecha = date.today(),Tipo_resultado = tipoRes )
        res.save()
    send_mailgun_message(m.correo,correosUsuarios,m.email_asunt,m.email_cuerpo)

def send_message_via_smtp(from_, to, mime_string):
    ''' sends a mime message to mailgun SMTP gateway '''
    smtp = smtplib.SMTP("smtp.mailgun.org", 587)
    smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
    smtp.sendmail(from_, to, mime_string)
    smtp.quit()


def send_mailgun_message(from_, to, subject, text, tag=None, track=True):
    ''' compose and sends a text-only message through mailgun '''
    msg = MIMEText(text, _charset='utf-8')

    msg['Subject'] = subject
    msg['From'] = from_
    msg['To'] = ", ".join(to)
    if tag:
        # you can attach tags to your messages
        msg['X-Mailgun-Tag'] = tag
    if track:
        # you can auto transform links to track clicks
        msg['X-Mailgun-Track'] = "yes"
    send_message_via_smtp(from_, to, msg.as_string())

def enviarWhatsapp(ID,mId):
    usuariasCamp,camp = contactosxcampa.objects.filter(campania = ID),Campania.objects.get(pk = ID)
    m,fechaActual = Medio.objects.get(pk=mId),date.today()
    for u in usuariasCamp:
        res = resultadosxcampania(contacto_cc=u.contacto,campania_id=camp,medio_id=m,fecha=fechaActual)
        res.save()
        clientWhatsapp.send_message(whatsapp_Template,"57"+u.contacto.celular,str(res.id))




def camp_activa(campId):
    fechaActual = date.today()
    camp = Campania.objects.get(pk = campId)
    estado = False 
    if camp.fechaInicio == fechaActual:
        e = estado_campania.objects.get(descripcion=1)
        camp.estado = e
        camp.save()
        estado = True

    return estado

def auxIntensidadMedio(campId,intensidad,medioxc):
    if intensidad == 1:
        crearTareaCampaña(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
    elif intensidad == 2:
        crearTareaCampaña(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
        crearTareaCampaña(campId,medioxc.hora2.hour,medioxc.hora2.minute,medioxc.medio_id.id)
    else:
        crearTareaCampaña(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
        crearTareaCampaña(campId,medioxc.hora2.hour,medioxc.hora2.minute,medioxc.medio_id.id)
        crearTareaCampaña(campId,medioxc.hora3.hour,medioxc.hora3.minute,medioxc.medio_id.id)


def crearTaskxmedioxcamp(campID):
    try:
        with transaction.atomic():
            medsxcamp = mediosxcampania.objects.filter(campania_id=campID)
            for m in medsxcamp:
                auxIntensidadMedio(campID,m.intensidad,m)
    except Exception as e:
        print("Error en el metodo de crear las tareas de una campaña")
        print(e)
        return e

def disableTaskxCamp(campID):
    camp = Campania.objects.get(pk = campID)
    print("Deshabilitanto la campaña")
    print(campID)
    for t in camp.tasksIds:
        idt = t
        if type(t) == list:
            idt = t[0]
        periodic_task = PeriodicTask.objects.get(pk = idt)
        periodic_task.enabled = False
        periodic_task.save()
        periodic_task.delete()
    inactiva = estado_campania.objects.get(descripcion=3)
    camp.estado = inactiva
    camp.save()      


def customSchedule(h,m):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=m,
        hour=h,
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
        timezone=pytz.timezone('America/Bogota'),
    )
    return schedule

@shared_task(name="check_camp_ini")
def check_camp_ini():
    print("--Chequeando campañas que inician--")
    campanias = Campania.objects.filter(estado = estado_campania.objects.get(descripcion=2))
    for c in campanias:
        if camp_activa(c.id) and len(c.tasksIds) == 0:
            crearTaskxmedioxcamp(c.id)
    print("--Chequeando campañas que inician--")

@shared_task(name="check_camp_fini")
def check_camp_fini():
    print("--Chequeando campañas que terminan--")
    campaniasList = Campania.objects.filter(estado = estado_campania.objects.get(descripcion=1))
    fechaActual = date.today()
    print("Lista de campañas a deshabilitar")
    print(campaniasList)
    for campania in campaniasList:
        if campania.fechaFin == fechaActual or campania.fechaFin < fechaActual:
            disableTaskxCamp(campania.id)
    print("--Chequeando campañas que terminan--")

@shared_task(name="enviar_sms")
def enviar_sms(campId,mId):
    envMensajeUsuarias(campId,mId)
    print("Enviando sms")

@shared_task(name="enviar_sms")
def enviar_sms(campId,mId):
    envMensajeUsuarias(campId,mId)
    print("Enviando sms")

@shared_task(name="llamadas")
def llamar(campId,mId,tel=''):
    llamar_usuarias(campId,mId,tel)
    print("Llamando")

@shared_task(name="enviar_wp")
def enviar_wp(campId,mId):
    enviarWhatsapp(campId,mId)
    print("Mensajes de wp Enviados")

@shared_task(name="correos")
def correos(campId,mId):
    enviar_correos(campId,mId)
    print("Correos enviados")

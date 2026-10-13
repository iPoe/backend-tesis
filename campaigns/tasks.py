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
from .models import Campania,estado_campania,mediosxcampania,Medio,contactosxcampa,resultadosxcampania,	Tipo_resultado, CampaignTask

from django_celery_beat.models import IntervalSchedule, PeriodicTask,CrontabSchedule
from .twilioAPI import VoiceCall,SMS,Email,WhatsApp

clientSMS = SMS()
clientVoice = VoiceCall()
newWhatsappClient = WhatsApp()
content_sid = 'HXc7e2769d37df6216c62cfb88d7aed6af'

def crearTareacampaigns(campId, hora, minute, mId, tel=""):
    cam = Campania.objects.get(pk=campId)
    m = Medio.objects.get(pk=mId)
    name = f"Task_{m.id}_{hora}_{minute}"

    schedule = customSchedule(hora, minute)
    
    task_name = ''
    task_args = [campId, mId]
    
    if m.tipo_medio.descripcion == 4: # SMS
        task_name = 'enviar_sms'
    elif m.tipo_medio.descripcion == 2: # Llamada Tel
        task_name = 'llamadas'
        task_args.append(1) # tel=1
    elif m.tipo_medio.descripcion == 1: # Llamada Cel
        task_name = 'llamadas'
    elif m.tipo_medio.descripcion == 3: # Correo
        task_name = 'correos'
    elif m.tipo_medio.descripcion == 5: # WhatsApp
        task_name = 'enviar_wp'
    
    if task_name:
        periodic_task = PeriodicTask.objects.create(
            crontab=schedule,
            name=name,
            task=task_name,
            args=json.dumps(task_args),
            start_time=datetime.datetime.now()
        )
        CampaignTask.objects.create(campania=cam, periodic_task_id=periodic_task.id, medio=m)

def llamar_usuarias(ID, mId, tel=''):
    # ⚡ Bolt: Removed duplicate queries and optimized N+1 (N+1 Optimization)
    # The original code fetched the campania twice using .get(), created outcomes twice,
    # fetched m.voicemedio as N+1, and referenced a non-existent numerosUsuarias variable.
    cons = contactosxcampa.objects.filter(campania=ID).select_related('contacto')
    # Use select_related to prevent N+1 query when accessing voicemedio
    m = Medio.objects.select_related('voicemedio').get(pk=mId)
    fechaActual = date.today()

    resultados = [
        resultadosxcampania(
            contacto_cc_id=obj.contacto_id,
            campania_id_id=ID,
            medio_id_id=mId,
            fecha=fechaActual
        )
        for obj in cons
    ]
    # bulk_create returns the objects with IDs populated when using PostgreSQL
    resultados_creados = resultadosxcampania.objects.bulk_create(resultados)

    m_voice = m.voicemedio
    matchUrlAudio = True if m_voice.audio_file else False
    mensajeVoz = m_voice.mensaje_texto
    urlAUdio = m_voice.audio_file.url if matchUrlAudio else ''

    numerosUsuarias = ["+57" + (obj.contacto.telefono if tel else obj.contacto.celular) for obj in cons]

    for n, res in enumerate(resultados_creados):
        clientVoice.voice_call(mensajeVoz, urlAUdio, numerosUsuarias[n], str(res.id))

def envMensajeUsuarias(ID,mId):
    # ⚡ Bolt: Prevent N+1 queries for 'contacto' (N+1 Optimization)
    # The original code executed N queries to access obj.contacto.celular.
    # Added select_related('contacto') to prefetch the data. Also assigned IDs directly for camp and m to bypass redundant queries.
    cons = contactosxcampa.objects.filter(campania = ID).select_related('contacto')
    m = Medio.objects.select_related('smsmedio').get(pk=mId)
    fechaActual = date.today()
    m_sms = m.smsmedio
    txt = m_sms.mensaje
    numerosUsuarias = ["+57"+obj.contacto.celular for obj in cons]
    cant = len(numerosUsuarias)

    res_list = [
        resultadosxcampania(contacto_cc_id=cons[n].contacto_id,campania_id_id=ID,medio_id_id=mId,fecha=fechaActual)
        for n in range(cant)
    ]
    created_res = resultadosxcampania.objects.bulk_create(res_list)

    for n, res in enumerate(created_res):
        clientSMS.send_message(txt, numerosUsuarias[n], str(res.id))

def enviar_correos(ID,mId):
    # ⚡ Bolt: Deduplicate redundant queries for 'contactosxcampa' (N+1/Redundant Optimization)
    # The original code fetched the same queryset twice ('usuariasCamp' and 'usuarios_campaña')
    # and additionally executed N+1 queries by missing select_related on 'contacto'.
    # We now fetch it once, use select_related('contacto') to prefetch the relation, and assign IDs directly to bypass redundant .get() queries for 'camp' and 'm'.
    usuarios_campaña = contactosxcampa.objects.filter(campania=ID).select_related('contacto')
    correosUsuarios = [ usuaria.contacto.email for usuaria in usuarios_campaña]

    # Bypass .get() for foreign keys since we already have the IDs
    tipoRes = Tipo_resultado.objects.get( descripcion = "si" )

    res_list = [
        resultadosxcampania(contacto_cc_id = usuario.contacto_id, campania_id_id = ID, medio_id_id = mId, fecha = date.today(),Tipo_resultado = tipoRes )
        for usuario in usuarios_campaña
    ]
    resultadosxcampania.objects.bulk_create(res_list)

    # We need Medio to get the emailmedio relation
    # Bolt: Select related to avoid N+1 for emailmedio
    m = Medio.objects.select_related('emailmedio').get(pk=mId)

    m_email = m.emailmedio
    send_mailgun_message(m_email.remitente, correosUsuarios, m_email.asunto, m_email.cuerpo)

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
    # ⚡ Bolt: Bypass redundant foreign key .get() queries (Optimization)
    # The original code fetched campania and medio using .get() to create the resultado records, but we only need their IDs.
    usuariasCamp = contactosxcampa.objects.filter(campania = ID).select_related('contacto')
    fechaActual = date.today()

    resultados = []
    for u in usuariasCamp:
        res = resultadosxcampania(contacto_cc_id=u.contacto_id,campania_id_id=ID,medio_id_id=mId,fecha=fechaActual)
        res.save()
        newWhatsappClient.send_content_message(
            content_sid,
            'MGfc684cdf8bd8a626ecf36c9e976c9055',
            "57" + u.contacto.celular,
            str(res.id)
        )




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
        crearTareacampaigns(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
    elif intensidad == 2:
        crearTareacampaigns(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
        crearTareacampaigns(campId,medioxc.hora2.hour,medioxc.hora2.minute,medioxc.medio_id.id)
    else:
        crearTareacampaigns(campId,medioxc.hora1.hour,medioxc.hora1.minute,medioxc.medio_id.id)
        crearTareacampaigns(campId,medioxc.hora2.hour,medioxc.hora2.minute,medioxc.medio_id.id)
        crearTareacampaigns(campId,medioxc.hora3.hour,medioxc.hora3.minute,medioxc.medio_id.id)


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
    camp = Campania.objects.get(pk=campID)
    print("Deshabilitanto la campaña")
    print(campID)
    campaign_tasks = CampaignTask.objects.filter(campania=camp)
    periodic_task_ids = list(campaign_tasks.values_list('periodic_task_id', flat=True))
    
    if periodic_task_ids:
        periodic_tasks = PeriodicTask.objects.filter(pk__in=periodic_task_ids)
        periodic_tasks.update(enabled=False)
        periodic_tasks.delete()

    campaign_tasks.delete()
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

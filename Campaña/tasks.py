import datetime
import pytz
import json

from celery import shared_task
from datetime import date
from .models import Campania,estado_campania,mediosxcampania,Medio,contactosxcampa,resultadosxcampania,Contacto
from django_celery_beat.models import IntervalSchedule, PeriodicTask,CrontabSchedule
from .twilioAPI import VoiceCall,SMS

clientSMS = SMS()
clientVoice = VoiceCall()


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
    else:
        schedule = customSchedule(hora,minute)
        llamadaCel= PeriodicTask.objects.create(
            crontab=schedule,            
            name=name,
            task='llamadas',
            args=json.dumps([campId,mId]),
            start_time=datetime.datetime.now()
        )
        idTask.append(llamadaCel.id)

    #idTask.append(sms_camp.id)
    cam.tasksIds += idTask
    cam.save()
    
        


def llamar_usuarias(ID,mId,tel=''):
    cons = contactosxcampa.objects.filter(campania = ID)

    m = Medio.objects.get(pk=mId)
    
    fechaActual = date.today()
    numerosUsuarias = ["+57"+obj.contacto.celular for obj in cons]
    if tel == 1:
        numerosUsuarias = ["+57"+obj.contacto.telefono for obj in cons]

    mensajeVoz = m.sms_mensaje
    #mensajeVoz = '¡Hola! Te llamamos desde Salud Pública, queremos darte la bienvenida a las nueva era digital de las llamadas automáticas, es un placer para mi hablarte, deseo que pronto nos conozcamos, ¡Muchas gracias! Y te deseo una Feliz Navidad y Próspero año nuevo, ¡Hasta luego y lindo día!'
    camp = Campania.objects.get(pk = ID)
    cant = len(numerosUsuarias)
    for n in range(cant):
        res = resultadosxcampania(contacto_cc=cons[n].contacto,campania_id=camp,medio_id=m,fecha=fechaActual)
        res.save()
        clientVoice.voice_call(mensajeVoz, '', numerosUsuarias[n], str(res.id))

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
    medsxcamp = mediosxcampania.objects.filter(campania_id=campID)
    for m in medsxcamp:
        auxIntensidadMedio(campID,m.intensidad,m)           

def disableTaskxCamp(campID):
    camp = Campania.objects.get(pk = campID)
    
    for t in camp.tasksIds:
        idt = t
        if type(t) == list:
            idt = t[0]
        periodic_task = PeriodicTask.objects.get(pk = idt)
        periodic_task.enabled = False
        periodic_task.save()
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

@shared_task(name="check_camp")
def check_camp():
    print("--Chequeando campañas--")
    campanias = Campania.objects.all()
    fechaActual = date.today()
    for c in campanias:
        print(c.tasksIds)

        if camp_activa(c.id) and len(c.tasksIds) == 0:
            crearTaskxmedioxcamp(c.id)
        else:
            pass
    for c in campanias:
        if c.fechaFin == fechaActual:
            disableTaskxCamp(c.id)
    print("--Chequeando campañas--")

@shared_task(name="enviar_sms")
def enviar_sms(campId,mId):
    envMensajeUsuarias(campId,mId)
    print("Enviando sms")

@shared_task(name="llamadas")
def llamar(campId,mId,tel=''):
    llamar_usuarias(campId,mId,tel)
    print("Llamando")

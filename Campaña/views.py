
from typing import Tuple
from urllib import response
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from datetime import date
import datetime as dt
from django.db.models import Count
from django.db import transaction
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import generate_access_token, generate_refresh_token
import traceback


#1cel,2tel,correo3,sms4,wp5
from .models import (Campania,
	Contacto, 
	Medio,
	contactosxcampa,
	Operador,
	mediosxcampania,
	Tipo_resultado,
	resultadosxcampania,
	estado_campania,
	Usuario
)
from .serializers import (CampañaSerializer,
	ContactosSerializer,
	contactosxcampSerializer,
	MediaSerializer,
	UsuarioSerializer
)
from .tasks import crearTareaCampaña
from Campaña.tasks import crearTaskxmedioxcamp,disableTaskxCamp
from .setup import Camp_setup
from twilio.twiml.messaging_response import MessagingResponse
from .twilioAPI import WhatsApp


clientWhatsapp = WhatsApp()

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
	data = request.data
	email,password = data['email'],data['clave']
	response = Response()
	if (email is None) or (password is None):
		raise exceptions.AuthenticationFailed('email and password required')
	
	operador = Usuario.objects.filter(email = email).first()
	if(operador is None):
		raise exceptions.AuthenticationFailed('user not found')
	if(not operador.clave == password):
		raise exceptions.AuthenticationFailed('wrong password')
	# serialized_user = UsuarioSerializer(operador)
	access_token = generate_access_token(operador)
	refresh_token = generate_refresh_token(operador)

	response .set_cookie(key='refreshtoken', value= refresh_token)
	response.data = {
		'acces_token' : access_token,
		'usuario' : operador.id,
	}
	return response



def change_estado_campania(ID):
	Camp = Campania.objects.get(pk = ID)
	fechaActual = date.today()
	if Camp.fechaInicio == fechaActual:
		Camp.estado = estado_campania.objects.get(descripcion=1)
	elif Camp.fechaInicio > fechaActual:
		Camp.estado = estado_campania.objects.get(descripcion=2)
	else:
		pass
	Camp.save()


@api_view(['GET'])
def recuento_camp(request):
	try:		
		data = {
			'finalizadas':0,
			'programadas':0,
			'activas':0,
			'total': Campania.objects.count()
		}
		query = Campania.objects.all().values('estado').annotate(total=Count('estado')).order_by('total')
		for e in query:
			if e['estado'] == 3:
				data['finalizadas'] = e['total']
			elif e['estado'] == 2:
				data['programadas'] = e['total']
			else:
				data['activas'] = e['total']
		return JsonResponse(data,status=201,safe=False)
	except Exception as e:
		print(e)
		return JsonResponse("Error en la URL de recuento",status=400,safe=False)

@api_view(['GET'])
def get_campanias(request):
	try:
		if request.method == 'GET':
			campanias = Campania.objects.all()
			serializer = CampañaSerializer(campanias,many=True)
			data = serializer.data
			for x in data:
				mxc = mediosxcampania.objects.filter(campania_id=x['id'])
				x.pop('operador_ID')
				x.pop('Fecha_Creada')
				if len(mxc)>0:
					medioSerializer = contactosxcampSerializer(mxc,many=True)
					x['medios'] = medioSerializer.data
					
			return JsonResponse(data,status=201,safe=False)
	except Exception as e:
		print(e)
		return JsonResponse("Error al obtener recuento campañas",status=201,safe=False)

@api_view(['PUT'])
def updateCamp(request):
	try:
		with transaction.atomic():
			if request.method == 'PUT':
				dataCamp = request.data
				fIni = dt.datetime.strptime(dataCamp['fechaInicio'], "%d-%m-%Y")
				fFini = dt.datetime.strptime(dataCamp['fechaFin'], "%d-%m-%Y")

				Campania.objects.filter(pk=dataCamp['id']).update(nombre = dataCamp['nombre'],fechaInicio=fIni,
				fechaFin=fFini,duracion=int(dataCamp['duracion']))
				#a.save()
				change_estado_campania(dataCamp['id'])
				c = Campania.objects.get(pk = dataCamp['id'])
				if c.estado.descripcion == 1 and len(c.tasksIds)==0:
					crearTaskxmedioxcamp(c.id)
				sercamp = CampañaSerializer(c)
				data = sercamp.data
				return JsonResponse(data,status=201,safe=False)
	except Exception as e:
		print(e)
		return JsonResponse("Error en actualizar camp",status=400,safe=False)

@api_view(['PUT'])
def endCamp(request):
	if request.method == 'PUT':
		try:
			with transaction.atomic():
				dataCamp = request.data
				c = Campania.objects.get(pk = dataCamp['id'])
				fFini,e = dt.datetime.strptime(dataCamp['fechaFin'], "%d-%m-%Y"),estado_campania.objects.get(descripcion=3)
				Campania.objects.filter(pk=dataCamp['id']).update(tasksIds = c.tasksIds,estado = e, fechaFin=fFini,duracion=int(dataCamp['duracion']))
				if c.estado.descripcion == 1:
					disableTaskxCamp(dataCamp['id'])
				sercamp = CampañaSerializer(c)
				data = sercamp.data
				return JsonResponse(data,status=201,safe=False)

		except Exception as e:
			print(e)
			return JsonResponse("Error en finalizar camp",status=400,safe=False)

@api_view(['POST','PATCH','GET'])
def campania_view(request):	

	if request.method=='GET':
		try:
			with transaction.atomic():
				campanias = Campania.objects.all()
				serializer = CampañaSerializer(campanias,many=True)
				data = serializer.data
				for x in data:
					mxc = mediosxcampania.objects.filter(campania_id=x['id'])
					x.pop('operador_ID')
					x.pop('Fecha_Creada')
					medioSerializer = contactosxcampSerializer(mxc,many=True)
					x['medios'] = medioSerializer.data
				return JsonResponse(data,status=201,safe=False)
		except Exception as e:
			print(e)
			return JsonResponse("Error en obtener camp",status=400,safe=False)



	elif request.method == 'POST':
		try:
			with transaction.atomic():
				mediosdata = request.data['medios']
				CampaniaConf = Camp_setup(request.data)
				if CampaniaConf.camp.is_valid():
					campaniaId = CampaniaConf.guardarContactos()
					CampaniaConf.guardarMedios(campaniaId,mediosdata)
					nuevaCampania = Campania.objects.get(pk = campaniaId)
					if nuevaCampania.estado.descripcion == 1:
						crearTaskxmedioxcamp(campaniaId)
					return JsonResponse(CampaniaConf.camp.data,status=201,safe=False)
		except Exception as e:
			print("Error en el metodo post para crear una campaña")
			print(e)
			traceback.print_exc()
			print(CampaniaConf.camp.errors)
			return JsonResponse(CampaniaConf.camp.errors,status=400,safe=False)

@api_view(['GET'])
def usuarias_existentes(request):
	if request.method == 'GET':
		usuarias_bd = contactosxcampa.objects.values('nombreContactos').annotate(dcount=Count('nombreContactos'))
		list_nombres = [ x['nombreContactos'] for x in usuarias_bd]
		return Response(list_nombres)

@api_view(['POST'])
def save_result(request):
	if request.method == 'POST':
		try:
			with transaction.atomic():
				data,textRes = request.data,"no"
				print(data)
				idres = int(data['idLlamada'])
				if data['res'] == 'completed' or data['res'] == 'delivered':
					textRes = "si"
				tipoRes = Tipo_resultado.objects.get(descripcion = textRes)
				res = resultadosxcampania.objects.update_or_create(pk = idres,defaults={'Tipo_resultado':tipoRes})
				return JsonResponse("Update completed",status=201,safe=False)
		except Exception as e:
			print(e)
			return JsonResponse("Error al guardar resultado Medio",status=400,safe=False)

@api_view(['POST'])
def login_operador(request):
	if request.method == 'POST':
		try:
			with transaction.atomic():

				data = request.data
				correo,password = data['email'],data['clave']
				
				operador = Operador.objects.filter(email = correo)
				
				if len(password)!=0 and len(operador)>0:
					
					if password != operador[0].clave:
						
						data = {
						'error':'Contraseña incorrecta',
						}
						return Response(data,status=400)

					else:
						data = {
						'email':correo,
						'id': operador[0].id,
						'token': 'beaker 123456789'
						

						}
						return Response(data)

				else:
					data = {
					'error': 'Correo o contraseña incorrectos',

					}
					return Response(data,status=400)
		except Exception as e:
			print(e)
			return JsonResponse("Error al iniciar sesion",status=400,safe=False)

def auxHMedio(idm):
	lista_horas = list()
	med = mediosxcampania.objects.get(pk=idm)
	#med = medxcam.medio_id
	if med.intensidad == 3:
		lista_horas = [med.hora1,med.hora2,med.hora3]
	elif med.intensidad == 2:
		lista_horas = [med.hora1,med.hora2]	
	else:
		lista_horas = [med.hora1]
	return lista_horas

def estaux(idcamp):
	campania = Campania.objects.get(pk = idcamp)
	serializer = CampañaSerializer(campania)
	dataest = serializer.data
	users = contactosxcampa.objects.filter(campania=campania)
	dataest['nombreContactos'] = users[0].nombreContactos
	mxc = mediosxcampania.objects.filter(campania_id=campania)
	dataest.pop('operador_ID')
	dataest.pop('Fecha_Creada')
	lista_medios = list()
	for m in mxc:
		dicMedio = {
			"tipoMedio":m.medio_id.tipo_medio.descripcion,
		"sms": m.medio_id.sms_mensaje,
		"intensidad": m.intensidad,
		"Horas": auxHMedio(m.id)
		}
		lista_medios.append(dicMedio)

	dataest['medios'] = lista_medios
	return dataest

@api_view(['POST','PUT'])
def test_estadisticas(request):
	if request.method == 'PUT':
		try:
			with transaction.atomic():

				idcampania = request.data['id']
				campania,dataest = Campania.objects.get(pk = idcampania),estaux(idcampania)
				resultadosCampania = resultadosxcampania.objects.filter(campania_id=campania).values('contacto_cc',
				'medio_id','Tipo_resultado').order_by('contacto_cc','medio_id')
				
				i = 1
				dicresxmed = {}
				if len(resultadosCampania) > 0:
					contacantiguo,listausers = resultadosCampania[0]['contacto_cc'],list()
					for res in resultadosCampania:
						#contactoActual = Contacto.objects.get(identidad=res['contacto_cc'])				
						if res['contacto_cc']!= contacantiguo:
							contSer = ContactosSerializer(Contacto.objects.get(identidad=contacantiguo))
							diccont = contSer.data
							dicfinal = {**diccont,**dicresxmed}
							listausers.append(dicfinal)
							dicresxmed,i = {},1
						strMedio = "medio_{}".format(i)
						if res['Tipo_resultado'] == 1:
							dicresxmed[strMedio] = "Si"
						elif res['Tipo_resultado'] == 3:
							dicresxmed[strMedio] = "R"
						else:
							dicresxmed[strMedio] = "No"
						# dicresxmed[strMedio] = "Si" if res['Tipo_resultado'] == 1 else "No"
						contacantiguo = res['contacto_cc']
						i+=1

					contSer = ContactosSerializer(Contacto.objects.get(identidad=contacantiguo))
					diccont = contSer.data
					dicfinal = {**diccont,**dicresxmed}
					listausers.append(dicfinal)
					dataest['estadistica'] = listausers
				else:
					dataest['estadistica'] = []

				return JsonResponse(dataest,status=201,safe=False)
				
		except Exception as e:
			print("Un error ocurrio en las estadisticas")
			print(e)
			return JsonResponse("Error al cargar las estadisticas",status=400,safe=False)
	elif request.method == 'POST':
		try:
			with transaction.atomic():
				data,textRes = request.data,"no"
				print(data)
				idres = int(data['idLlamada'])
				if data['res'] == 'completed' or data['res'] == 'delivered':
					textRes = "si"
				tipoRes = Tipo_resultado.objects.get(descripcion = textRes)
				res = resultadosxcampania.objects.update_or_create(pk = idres,defaults={'Tipo_resultado':tipoRes})
				return JsonResponse("Update completed",status=201,safe=False)
		except Exception as e:
			print(e)
			return JsonResponse("Error al guardar resultado Medio",status=400,safe=False)

@api_view(['POST'])
def reply_whatsapp(request):
	if request.method == 'POST':
		try:
			usuaria = Contacto.objects.filter(celular=request.data['WaId'][2:]).first()
			campañas_usuaria = contactosxcampa.objects.filter(contacto=usuaria)
			estado_activo = estado_campania.objects.get(descripcion=1)
			campañas_activas = [ camp.campania for camp in campañas_usuaria if camp.campania.estado == estado_activo]
			print(campañas_activas)
			if len(campañas_activas):
				for campania in campañas_activas:
					aux_reply(campania,usuaria)
				return JsonResponse("Respuesta de whatsapp enviada",status=201,safe=False)
		except Exception as e:
			print(e)
			traceback.print_exc()
			return JsonResponse("Error al responder al wp",status=400,safe=False)

def aux_reply(campania, usuaria):
	medsxcamp = mediosxcampania.objects.filter(campania_id = campania.id)
	medios = [ Medio.objects.get(pk = m.medio_id.id) for m in medsxcamp]
	wp_medios = [ medio for medio in medios if medio.tipo_medio.descripcion == 5 ]
	tipoRes = Tipo_resultado.objects.get( descripcion = "r" )

	for medio in wp_medios:
		res = resultadosxcampania.objects.update_or_create(
			contacto_cc=usuaria.identidad,
			campania_id = campania.id, 
			medio_id= medio.id, 
			defaults=	{'Tipo_resultado' : tipoRes} 
		)
		clientWhatsapp.send_message( medio.sms_mensaje ,"57"+usuaria.celular)

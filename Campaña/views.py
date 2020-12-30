
from django.http import HttpResponse,JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from datetime import date
import datetime as dt
from django.db.models import Count
from django.db import transaction


#1cel,2tel,correo3,sms4,wp5
from .models import Campania,Contacto,contactosxcampa,Operador,mediosxcampania,Tipo_resultado,resultadosxcampania,estado_campania
from .serializers import CampañaSerializer,ContactosSerializer,contactosxcampSerializer,MediaSerializer
from .tasks import crearTareaCampaña
from Campaña.tasks import crearTaskxmedioxcamp,disableTaskxCamp

from .setup import Camp_setup

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
	

	if request.method == 'PATCH':
		cam = Campania.objects.get(pk=data['id'])
		if cam.estado == 1:
			cam.fechaFin = data['fechaFin']
			cam.duracion = cam.fechaFin.day - cam.fechaInicio.day
		else:
			cam.fechaInicio,cam.fechaFin= data['fechaInicio'],data['fechaFin']
			cam.duracion = cam.fechaFin.day - cam.fechaInicio.day
			estado_campaña(camp.id)

	elif request.method=='GET':
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
				if CampaniaConf.serializerCampania.is_valid():
					a = CampaniaConf.guardarContactos()
					r = CampaniaConf.guardarMedios(a,mediosdata)
					if CampaniaConf.camp.estado.descripcion == 1:
						crearTaskxmedioxcamp(a)
					return JsonResponse(CampaniaConf.serializerCampania.data,status=201,safe=False)

			#return JsonResponse(CampaniaConf.serializerCampania.errors,status=400,safe=False)
		except Exception as e:
			print(e)
			return JsonResponse(CampaniaConf.serializerCampania.errors,status=400,safe=False)



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





@api_view(['POST'])
def estadisticas_campaña(request):
	if request.method == 'POST':
		try:
			with transaction.atomic():

				data =  request.data
				idcamp = int(data['id'])
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

				#Sacar las estadisticas por usuarias
				statxUsuarias = list()
				fini,fechaAct = campania.fechaInicio,date.today()


				if campania.estado.descripcion == 1  or campania.estado.descripcion == 3:
					#print(campania)
					userscamp = contactosxcampa.objects.filter(campania=campania)
					
					for u in userscamp:
						#print(u)
						i = 1				
						strMedio = "medio_{}".format(i)
						contSer = ContactosSerializer(u.contacto)
						diccont = contSer.data
						fechanueva = campania.fechaInicio
						dicresmed = {}
						while fechanueva <= fechaAct and fechanueva <= campania.fechaFin:				
							for m in mxc:
								resMed = []
								res = resultadosxcampania.objects.filter(contacto_cc = u.contacto,
								campania_id=campania,fecha=fechanueva,medio_id=m.medio_id).values('Tipo_resultado')
								#print(res)	
								if len(res)!=0:
									resMed = [r['Tipo_resultado'] for r in res]
									for txt in resMed:
										txtaux = "Si"
										if txt == None:
												txtaux = ""
										elif txt == 2:
												txtaux = "No"
										diccont[strMedio] = txtaux
										i += 1
										strMedio = "medio_{}".format(i)

							d = fechanueva.day
							fechanueva = fechanueva.replace(day = d + 1)
						statxUsuarias.append(diccont)
					dataest['estadistica'] = statxUsuarias
		except Exception as e:
			print(e)
			return JsonResponse("Error al generar estadistica",status=400,safe=False)



				
		return JsonResponse(dataest,status=201,safe=False)


@api_view(['POST'])
def test_estadisticas(request):
	try:
		with transaction.atomic():
			idcampania = request.data['id']
			campania = Campania.objects.get(pk = idcampania)
			resultadosCampania = resultadosxcampania.objects.filter(campania_id=campania).values('contacto_cc',
			'medio_id','Tipo_resultado').order_by('contacto_cc','medio_id')
			print(resultadosCampania)
			contacantiguo,listausers = resultadosCampania[0]['contacto_cc'],list()
			i,flag,size = 1,0,len(resultadosCampania)
			dicresxmed = {}
			for res in resultadosCampania:
				contactoActual = Contacto.objects.get(identidad=res['contacto_cc'])
				if res['contacto_cc']!= contacantiguo or flag == size:
					contSer = ContactosSerializer(Contacto.objects.get(identidad=contactoActual))
					diccont = contSer.data
					dicfinal = {**diccont,**dicresxmed}
					listausers.append(dicfinal)
					dicresxmed,i = {},0
				strMedio = "medio_{}".format(i)
				dicresxmed[strMedio] = "si" if res['Tipo_resultado'] == 1 else "no"
				contacantiguo,i = res['contacto_cc'],i+1
				flag+=1
				#listausers.append(dicresxmed)

			
				
				


			return JsonResponse(listausers,status=201,safe=False)
			
	except Exception as e:
		print(e)
		return JsonResponse("Chale algo fallo xd :'v",status=201,safe=False)
		


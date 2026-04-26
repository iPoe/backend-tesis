import datetime
from .models import Campania, estado_campania


def chequear_estado_campaña():
	print("----Mirando estado campañas----")
	#Mirar todas las campañas y mirar si la fecha de inicio ya se cumplio
	#Si fecha actual == fecha inicio, entonces estado_campaña = Activo (1)
	fecha_actual = datetime.date.today()
	try:
		estado_programado = estado_campania.objects.get(descripcion=2)
		estado_activo = estado_campania.objects.get(descripcion=1)

		Campania.objects.filter(
			estado=estado_programado,
			fechaInicio__lte=fecha_actual
		).update(estado=estado_activo)
	except estado_campania.DoesNotExist:
		pass
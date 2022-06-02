from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
	email = models.EmailField(verbose_name="email", max_length=20, unique=True)
	clave = models.CharField(max_length=20)
	def __str__(self):
		return self.email

class estado_campania(models.Model):
	#Va a ser por indicador 1:Activo 2:Programado 3:Finalizado
	descripcion = models.IntegerField(primary_key=True,unique=True)
	def __str__(self):
		return str(self.descripcion)


class Operador(models.Model):
	email = models.EmailField(verbose_name="email", max_length=20, unique=True)
	clave = models.CharField(max_length=20)
	def __str__(self):
		return self.email

class Campania(models.Model):

	nombre = models.CharField(max_length=30) #Preguntarle si el nombre debe ser unico
	Fecha_Creada = models.DateField()
	fechaInicio = models.DateField()
	fechaFin = models.DateField()
	duracion = models.IntegerField()
	operador_ID = models.ForeignKey(Operador,on_delete=models.PROTECT)
	estado = models.ForeignKey(estado_campania,on_delete=models.PROTECT)
	tasksIds = ArrayField(ArrayField(models.IntegerField()),null=True,blank=True,default=list)
	def __str__(self):
		return self.nombre

class Contacto(models.Model):
	identidad = models.CharField(primary_key=True,max_length=50)
	nombre = models.CharField(max_length=50)
	fecha_nacimiento = models.DateField(default=None)
	celular = models.CharField(default=None,max_length=10)
	telefono = models.CharField(default=None,max_length=15)
	email = models.EmailField(verbose_name="email")



class contactosxcampa(models.Model):
	campania = models.ForeignKey(Campania,on_delete=models.CASCADE,null=True)
	contacto = models.ForeignKey(Contacto,on_delete= models.PROTECT,null=True)
	nombreContactos = models.CharField(max_length=25,null=True)




class Tipo_medio(models.Model):
	descripcion = models.IntegerField()
	def __str__(self):
		return str(self.descripcion)

class Medio(models.Model):
	email_asunt = models.CharField(max_length=30,null=True,blank=True)
	correo = models.CharField(max_length=30,null=True,blank=True)
	email_cuerpo = models.CharField(max_length=500,null=True,blank=True)
	sms_mensaje = models.CharField(max_length=500,null=True,blank=True)
	llamada_aud = models.FileField(upload_to='audios/',null=True,blank=True)
	tipo_medio = models.ForeignKey(Tipo_medio,on_delete=models.PROTECT)
	def __str__(self):
		return str(self.id)

class Tipo_resultado(models.Model):
	descripcion = models.CharField(max_length=3,null=True,blank=True)

class resultadosxcampania(models.Model):
	contacto_cc = models.ForeignKey(Contacto,on_delete=models.PROTECT)
	campania_id = models.ForeignKey(Campania,on_delete=models.PROTECT)
	medio_id = models.ForeignKey(Medio,on_delete=models.PROTECT)
	fecha = models.DateField()
	Tipo_resultado = models.ForeignKey(Tipo_resultado,on_delete=models.PROTECT,null=True,blank=True)


class mediosxcampania(models.Model):
	campania_id = models.ForeignKey(Campania,on_delete=models.PROTECT)
	medio_id = models.ForeignKey(Medio,on_delete=models.PROTECT)
	intensidad = models.IntegerField()
	hora1 = models.TimeField(null=True,blank=True)
	hora2 = models.TimeField(null=True,blank=True)
	hora3 = models.TimeField(null=True,blank=True)


class resultadosxmedio(models.Model):
	tipo_resultado = models.ForeignKey(Tipo_resultado,on_delete=models.PROTECT)
	TipoMedio = models.ForeignKey(Tipo_medio,on_delete=models.PROTECT)
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    clave = models.CharField(max_length=100)
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None or not self.clave.startswith('pbkdf2_sha256$'):
            self.clave = make_password(self.clave)
        super().save(*args, **kwargs)

class estado_campania(models.Model):
    #Va a ser por indicador 1:Activo 2:Programado 3:Finalizado
    descripcion = models.IntegerField(primary_key=True,unique=True)
    def __str__(self):
        return str(self.descripcion)


class Operador(models.Model):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    clave = models.CharField(max_length=100)
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk is None or not self.clave.startswith('pbkdf2_sha256$'):
            self.clave = make_password(self.clave)
        super().save(*args, **kwargs)

class Campania(models.Model):

    nombre = models.CharField(max_length=30) #Preguntarle si el nombre debe ser unico
    Fecha_Creada = models.DateField(auto_now_add=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    duracion = models.IntegerField()
    operador_ID = models.ForeignKey(Operador,on_delete=models.PROTECT)
    estado = models.ForeignKey(estado_campania,on_delete=models.PROTECT)

class CampaignTask(models.Model):
    campania = models.ForeignKey(Campania, on_delete=models.CASCADE, related_name='tasks')
    periodic_task_id = models.IntegerField()
    # To track which specialized media this task belongs to
    medio = models.ForeignKey('Medio', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.campania.nombre} - {self.periodic_task_id}"

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
    tipo_medio = models.ForeignKey(Tipo_medio, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.tipo_medio} - {self.id}"

class EmailMedio(Medio):
    asunto = models.CharField(max_length=100, null=True, blank=True)
    remitente = models.EmailField(null=True, blank=True)
    cuerpo = models.TextField(null=True, blank=True)

class SMSMedio(Medio):
    mensaje = models.TextField(null=True, blank=True)

class WhatsAppMedio(Medio):
    mensaje = models.TextField(null=True, blank=True)

class VoiceMedio(Medio):
    mensaje_texto = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='audios/', null=True, blank=True)

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


# class resultadosxmedio(models.Model):
#     tipo_resultado = models.ForeignKey(Tipo_resultado,on_delete=models.PROTECT)
#     TipoMedio = models.ForeignKey(Tipo_medio,on_delete=models.PROTECT)
# from typing_extensions import required
from rest_framework import serializers
from datetime import date
import datetime
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import (Campania,
	Contacto,
	Medio,
	estado_campania,
	mediosxcampania,
	Tipo_medio,
	Usuario
)

class UsuarioSerializer(serializers.ModelSerializer):
	class Meta:
		model = Usuario
		fields = ['email']


def removerTags(s):
	sP = s.replace('<p>','')
	res = sP.replace('</p>','')
	return res


class CampañaSerializer(serializers.ModelSerializer):
	Fecha_Creada = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',])
	fechaFin = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',])
	fechaInicio = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',])
	duracion = serializers.IntegerField()
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = Campania
		fields = ['id','nombre','Fecha_Creada',
			'fechaInicio','fechaFin','duracion','operador_ID','estado']

	def create(self,validated_data):
		f_ini,f_actual = validated_data['fechaInicio'],date.today()
		if f_actual == f_ini:
			validated_data['estado'] = estado_campania.objects.get(descripcion = 1)
		else:
			validated_data['estado'] = estado_campania.objects.get(descripcion = 2)
		return Campania.objects.create(**validated_data)



class ContactosSerializer(serializers.ModelSerializer):
	fecha_nacimiento = serializers.DateField(input_formats=['%d/%m/%Y'])
	nombre = serializers.CharField(max_length=50)
	class Meta:
		model = Contacto
		fields = ['identidad', 'nombre','fecha_nacimiento','celular','email','telefono']
		extra_kwargs = {
            'identidad': {
                'validators': [],
            }
        }

	def create(self,validated_data):
		contacto, created = Contacto.objects.update_or_create(identidad=validated_data['identidad'],
			defaults={"nombre":validated_data['nombre'],"celular":validated_data['celular'],"telefono":validated_data['telefono'],"email":validated_data['email'],"fecha_nacimiento":validated_data['fecha_nacimiento']})
		return contacto


class MediaSerializer(serializers.ModelSerializer):
	llamada_aud = serializers.FileField(allow_empty_file=True,required=False)
	email_asunt = serializers.CharField(allow_blank=True,required=False)
	email_cuerpo = serializers.CharField(allow_blank=True,required=False)
	sms = serializers.CharField(allow_blank=True,required=False,source='sms_mensaje')
	tipoMedio = serializers.IntegerField(source='tipo_medio')
	intensidad = serializers.IntegerField()
	Horas = serializers.ListField(child = serializers.TimeField())
	campID = serializers.IntegerField()

	class Meta:
		model = Medio
		fields = ['sms','tipoMedio','llamada_aud','intensidad','Horas','campID','email_asunt','email_cuerpo']
	def create(self,validated_data):
		i = validated_data['tipo_medio']
		idcam = validated_data['campID']
		if i == 3:
			asunto = validated_data['email_asunt']
			cuerpo = validated_data['email_cuerpo']
			validated_data['email_asunt'] = removerTags(asunto)
			validated_data['email_cuerpo'] = removerTags(cuerpo)

		validated_data['tipo_medio'] = Tipo_medio.objects.get(descripcion=i)
		intensidadMed = (validated_data['intensidad'],validated_data['Horas'])
		validated_data.pop('intensidad')
		validated_data.pop('Horas')
		validated_data.pop('campID')
		medios = Medio.objects.create(**validated_data)
		campania = Campania.objects.get(pk = idcam)
		v = len(intensidadMed)
		
		i = intensidadMed
		if i[0] == 1:
			m = mediosxcampania.objects.create(campania_id=campania,
				medio_id=medios,
				intensidad=i[0],
				hora1=i[1][0])
			m.save()
		elif i[0] == 2:
			m = mediosxcampania.objects.create(campania_id=campania,
				medio_id=medios,
				intensidad=i[0],
				hora1=i[1][0],hora2=i[1][1])
			m.save()
		else:
			m = mediosxcampania.objects.create(campania_id=campania,
				medio_id=medios,
				intensidad=i[0],
				hora1=i[1][0],hora2=i[1][1],hora3=i[1][2])
			m.save()

		return medios


class contactosxcampSerializer(serializers.ModelSerializer):
	id = serializers.CharField(source='medio_id.tipo_medio')
	class Meta:
		model = mediosxcampania
		fields = ['id','intensidad']

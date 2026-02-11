# from typing_extensions import required
from rest_framework import serializers
from datetime import date
import datetime
from django.contrib.auth.validators import UnicodeUsernameValidator
from .models import (Campania,
	Contacto,
	Medio,
	EmailMedio, SMSMedio, WhatsAppMedio, VoiceMedio,
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


class campaignsSerializer(serializers.ModelSerializer):
	Fecha_Creada = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',], read_only=True)
	fechaFin = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',])
	fechaInicio = serializers.DateField(format="%d-%m-%Y",input_formats=['%d-%m-%Y',])
	duracion = serializers.IntegerField()
	id = serializers.IntegerField(read_only=True)

	class Meta:
		model = Campania
		fields = ['id','nombre','Fecha_Creada',
			'fechaInicio','fechaFin','duracion','operador_ID','estado']
		read_only_fields = ['estado']

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
    llamada_aud = serializers.FileField(allow_empty_file=True, required=False)
    sms = serializers.CharField(allow_blank=True, required=False)
    tipoMedio = serializers.IntegerField(source='tipo_medio.descripcion', read_only=True)
    tipo_medio_id = serializers.IntegerField(write_only=True)
    intensidad = serializers.IntegerField(write_only=True)
    Horas = serializers.ListField(child=serializers.TimeField(), write_only=True)
    campID = serializers.IntegerField(write_only=True)
    email_asunt = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email_cuerpo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    correo = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Medio
        fields = ['sms', 'tipoMedio', 'tipo_medio_id', 'llamada_aud', 'intensidad', 'Horas', 'campID', 'email_asunt', 'email_cuerpo', 'correo']
        extra_kwargs = {
            'email_asunt': {'required': False},
            'email_cuerpo': {'required': False},
            'correo': {'required': False},
        }

    def create(self, validated_data):
        tipo_medio_desc = validated_data.pop('tipo_medio_id')
        idcam = validated_data.pop('campID')
        intensidad = validated_data.pop('intensidad')
        horas = validated_data.pop('Horas')
        
        tipo_medio = Tipo_medio.objects.get(descripcion=tipo_medio_desc)
        
        # Determine specialized model
        if tipo_medio_desc == 3: # Email
            medio = EmailMedio.objects.create(
                tipo_medio=tipo_medio,
                asunto=removerTags(validated_data.get('email_asunt', '')),
                cuerpo=removerTags(validated_data.get('email_cuerpo', '')),
                remitente=validated_data.get('correo', '')
            )
        elif tipo_medio_desc == 4: # SMS
            medio = SMSMedio.objects.create(
                tipo_medio=tipo_medio,
                mensaje=validated_data.get('sms', '')
            )
        elif tipo_medio_desc == 5: # WhatsApp
            medio = WhatsAppMedio.objects.create(
                tipo_medio=tipo_medio,
                mensaje=validated_data.get('sms', '')
            )
        elif tipo_medio_desc in [1, 2]: # Voice (Cell/Tel)
            medio = VoiceMedio.objects.create(
                tipo_medio=tipo_medio,
                mensaje_texto=validated_data.get('sms', ''), # Using sms field for text-to-speech if no audio
                audio_file=validated_data.get('llamada_aud', None)
            )
        else:
            medio = Medio.objects.create(tipo_medio=tipo_medio)

        campania = Campania.objects.get(pk=idcam)
        
        # Create mediosxcampania entry
        mxc_params = {
            'campania_id': campania,
            'medio_id': medio,
            'intensidad': intensidad,
            'hora1': horas[0] if len(horas) > 0 else None,
            'hora2': horas[1] if len(horas) > 1 else None,
            'hora3': horas[2] if len(horas) > 2 else None,
        }
        mediosxcampania.objects.create(**mxc_params)

        return medio


class contactosxcampSerializer(serializers.ModelSerializer):
	id = serializers.CharField(source='medio_id.tipo_medio')
	class Meta:
		model = mediosxcampania
		fields = ['id','intensidad']

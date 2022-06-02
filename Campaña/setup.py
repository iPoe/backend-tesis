from typing import List
from Campaña.models import Campania,contactosxcampa
from .serializers import CampañaSerializer,ContactosSerializer,MediaSerializer
from django.db import transaction
import traceback

class Camp_setup:
    def __init__(self,data):
        self.data_contactos = data['contactos']
        self.data_medios = data['medios']
        self.datacamp = data
        self.datacamp.pop('contactos')
        self.datacamp.pop('medios')
        self.camp = CampañaSerializer(data = self.datacamp)
        self.serializerContactos = ContactosSerializer

    def guardarContactos(self):
        dcontactos = self.data_contactos
        for x in dcontactos:
            x['celular'] = str(x['celular'])
            x['telefono'] = str(x['telefono'])
        self.serializerContactos = ContactosSerializer(data=dcontactos,many=True)
        try:
            with transaction.atomic():
                if self.serializerContactos.is_valid() and self.camp.is_valid():
                    campania = self.camp.save()
                    if campania.estado.descripcion == 1:
                        contactos = self.serializerContactos.save()
                        objs = [contactosxcampa(
                            campania = Campania.objects.get(pk = campania.id),
                            contacto = contacto,nombreContactos=self.datacamp['nombreContactos'])
                            for contacto in contactos
                        ]
                        contactosxcampa.objects.bulk_create(objs)
                    print("ID DE LA CAMPANIA: ")
                    print(campania.id)
                    return campania.id
        except Exception as e:
            print("Exception enconuntered in save contacts func")
            print(e)
            return self.serializerContactos.errors

    
    def guardarMedios(self,ID,data):
        data_medios = data
        try:
            with transaction.atomic():
                idcam = Campania.objects.get(pk=ID).id
                for m in data_medios:
                    m['campID']= idcam
                crear_medio(data_medios)
        except Exception as e:
            print("exception Encountered in create media func")
            print(e)
            traceback.print_exc()

def crear_medio(data_medios):
    medios = []
    for medio in data_medios:
        medio_serializado = MediaSerializer( data = medio )
        if medio_serializado.is_valid():
            medios.append(medio_serializado.save())
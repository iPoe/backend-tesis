from Campaña.models import Campania,Medio,mediosxcampania,contactosxcampa
from .serializers import CampañaSerializer,ContactosSerializer,contactosxcampSerializer,MediaSerializer
from django.db import transaction
import sys
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
        self.mediosSerial = MediaSerializer

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
                print("Data recibida del medio")
                print(data_medios)
                print("Data recibida del medio")
                self.mediosSerial = MediaSerializer(data=data_medios,many=True)
                print("Info del medio serializer")
                print(self.mediosSerial)
                print(self.mediosSerial.is_valid())
                print("Info del medio serializer")
                if self.mediosSerial.is_valid():
                    print("Entro al if para guardar el medio")
                    medios = self.mediosSerial.save()
                    print(medios)
                    print("Medios Creados!")
        except Exception as e:
            print("exception Encountered in create media func")
            print(e)
            # type, value, traceback = sys.exc_info()
            # print('Error trace %s: %s' % (value, traceback))
            traceback.print_exc()
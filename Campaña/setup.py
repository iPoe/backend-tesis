from Campaña.models import Campania,Medio,mediosxcampania,contactosxcampa
from .serializers import CampañaSerializer,ContactosSerializer,contactosxcampSerializer,MediaSerializer
from django.db import transaction


class Camp_setup:
    #Cosas por añadir
    def __init__(self,data):
        self.data_contactos = data['contactos']
        self.data_medios = data['medios']
        self.datacamp = data
        self.datacamp.pop('contactos')
        self.datacamp.pop('medios')
        self.serializerCampania = CampañaSerializer(data = self.datacamp)
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
                if self.serializerContactos.is_valid():
                    self.camp = self.serializerCampania.save()
                    self.camp.tasksIds = []
                    self.camp.save()
                    if self.camp.estado.descripcion == 1:
                        contactos = self.serializerContactos.save()
                        objs = [contactosxcampa(
                            campania = self.camp,
                            contacto =c,nombreContactos=self.datacamp['nombreContactos'])
                            for c in contactos
                        ]
                        contactosxcampa.objects.bulk_create(objs)
                    return self.camp.id
        except Exception as e:
            print(e)
            print(self.serializerCampania)
            print(self.serializerContactos)
            return self.serializerContactos.errors

    
    def guardarMedios(self,ID,data):
        dmedios = data
        try:
            with transaction.atomic():
                idcam = Campania.objects.get(pk=ID).id
                for m in dmedios:
                    m['campID']= idcam
                #print(dmedios)
                self.mediosSerial = MediaSerializer(data=dmedios,many=True)
                if self.mediosSerial.is_valid():
                    self.mediosSerial.save()
                    return "Medios Creados!"
                else:
                    print(self.mediosSerial.errors)
                    return self.mediosSerial.errors
        except Exception as e:
            print(e)
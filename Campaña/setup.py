from Campaña.models import Campania,Medio,mediosxcampania,contactosxcampa
from .serializers import CampañaSerializer,ContactosSerializer,contactosxcampSerializer,MediaSerializer
from django.db import transaction


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
        print("DATA DE LA CAMPANIA")
        print("La data de la campania es: \n")
        print(self.datacamp)
        print("EL serializes dice:\n")
        print(self.camp.is_valid())
        print(self.camp)
        dcontactos = self.data_contactos
        for x in dcontactos:
            x['celular'] = str(x['celular'])
            x['telefono'] = str(x['telefono'])
        self.serializerContactos = ContactosSerializer(data=dcontactos,many=True)
        try:
            with transaction.atomic():
                if self.serializerContactos.is_valid():
                    self.camp.tasksIds = []
                    campania = self.camp.save()
                    if self.camp.estado.descripcion == 1:
                        contactos = self.serializerContactos.save()
                        objs = [contactosxcampa(
                            campania = campania.id,
                            contacto =c,nombreContactos=self.datacamp['nombreContactos'])
                            for c in contactos
                        ]
                        contactosxcampa.objects.bulk_create(objs)
                    print(self.camp.id)
                    return self.camp.id
        except Exception as e:
            print("Exception enconuntered")
            print(e)
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
            print("exception Encountered in create media func")
            print(e)
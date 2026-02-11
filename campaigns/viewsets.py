from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Count
from django.http import JsonResponse
from datetime import date
import datetime as dt
import traceback

from .models import (
    Campania, Contacto, Medio, EmailMedio, SMSMedio, WhatsAppMedio, 
    VoiceMedio, mediosxcampania, Tipo_medio, estado_campania, 
    resultadosxcampania, Tipo_resultado, CampaignTask
)
from .serializers import (
    campaignsSerializer, ContactosSerializer, MediaSerializer, 
    contactosxcampSerializer
)
from .tasks import crearTaskxmedioxcamp, disableTaskxCamp
from .setup import Camp_setup
from .twilioAPI import RestAccount

clientAccount = RestAccount()

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campania.objects.all()
    serializer_class = campaignsSerializer

    def get_queryset(self):
        # Override if needed, e.g., for filtering by operator
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for x in data:
            mxc = mediosxcampania.objects.filter(campania_id=x['id'])
            x.pop('operador_ID', None)
            x.pop('Fecha_Creada', None)
            medioSerializer = contactosxcampSerializer(mxc, many=True)
            x['medios'] = medioSerializer.data
        return Response(data)

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                mediosdata = request.data.get('medios', [])
                camp_setup = Camp_setup(request.data)
                if camp_setup.camp.is_valid():
                    campania_id = camp_setup.guardarContactos()
                    camp_setup.guardarMedios(campania_id, mediosdata)
                    
                    instance = Campania.objects.get(pk=campania_id)
                    if instance.estado.descripcion == 1:
                        crearTaskxmedioxcamp(campania_id)
                        
                    return Response(camp_setup.camp.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(camp_setup.camp.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data = request.data
            
            # Custom update logic from old updateCamp
            if 'fechaInicio' in data:
                data['fechaInicio'] = dt.datetime.strptime(data['fechaInicio'], "%d-%m-%Y").date()
            if 'fechaFin' in data:
                data['fechaFin'] = dt.datetime.strptime(data['fechaFin'], "%d-%m-%Y").date()
            
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            # Post-update logic (changing state and starting tasks if needed)
            instance = self.get_object()
            self._update_state(instance)
            
            if instance.estado.descripcion == 1 and not CampaignTask.objects.filter(campania=instance).exists():
                crearTaskxmedioxcamp(instance.id)
                
            return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def end(self, request, pk=None):
        instance = self.get_object()
        with transaction.atomic():
            e = estado_campania.objects.get(descripcion=3)
            instance.estado = e
            if 'fechaFin' in request.data:
                instance.fechaFin = dt.datetime.strptime(request.data['fechaFin'], "%d-%m-%Y").date()
            if 'duracion' in request.data:
                instance.duracion = int(request.data['duracion'])
            instance.save()
            
            disableTaskxCamp(instance.id)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = {
            'finalizadas': 0,
            'programadas': 0,
            'activas': 0,
            'total': Campania.objects.count(),
            'balance': clientAccount.get_account_balance()
        }
        query = Campania.objects.all().values('estado').annotate(total=Count('estado')).order_by('total')
        for e in query:
            if e['estado'] == 3:
                data['finalizadas'] = e['total']
            elif e['estado'] == 2:
                data['programadas'] = e['total']
            else:
                data['activas'] = e['total']
        return Response(data)

    @action(detail=True, methods=['get', 'put'])
    def statistics(self, request, pk=None):
        instance = self.get_object()
        if request.method == 'GET' or request.method == 'PUT':
            # This replicates the logic from old test_estadisticas
            dataest = self._get_base_stats(instance)
            resultados = resultadosxcampania.objects.filter(campania_id=instance).values(
                'contacto_cc', 'medio_id', 'Tipo_resultado'
            ).order_by('contacto_cc', 'medio_id')

            if len(resultados) > 0:
                listausers = []
                contacantiguo = resultados[0]['contacto_cc']
                dicresxmed = {}
                i = 1
                for res in resultados:
                    if res['contacto_cc'] != contacantiguo:
                        contSer = ContactosSerializer(Contacto.objects.get(identidad=contacantiguo))
                        dicfinal = {**contSer.data, **dicresxmed}
                        listausers.append(dicfinal)
                        dicresxmed, i = {}, 1
                    
                    strMedio = f"medio_{i}"
                    tipo_resultado = res['Tipo_resultado']
                    # Map from DB values to display values if needed
                    dic_resultados = {1: "1", 2: "5", 6: "3", 4: "2", 5: "4", 3: "1", 9: "Si", 10: "No"}
                    dicresxmed[strMedio] = dic_resultados.get(tipo_resultado, str(tipo_resultado))
                    
                    contacantiguo = res['contacto_cc']
                    i += 1

                contSer = ContactosSerializer(Contacto.objects.get(identidad=contacantiguo))
                dicfinal = {**contSer.data, **dicresxmed}
                listausers.append(dicfinal)
                dataest['estadistica'] = listausers
            else:
                dataest['estadistica'] = []

            return Response(dataest)

    def _get_base_stats(self, instance):
        serializer = self.get_serializer(instance)
        data = serializer.data
        users = contactosxcampa.objects.filter(campania=instance)
        if users.exists():
            data['nombreContactos'] = users[0].nombreContactos
        
        mxc = mediosxcampania.objects.filter(campania_id=instance)
        lista_medios = []
        for m in mxc:
            dicMedio = {
                "tipoMedio": m.medio_id.tipo_medio.descripcion,
                "sms": m.medio_id.smsmedio.mensaje if hasattr(m.medio_id, 'smsmedio') else 
                       (m.medio_id.whatsappmedio.mensaje if hasattr(m.medio_id, 'whatsappmedio') else ""),
                "intensidad": m.intensidad,
                "Horas": self._get_hours(m)
            }
            lista_medios.append(dicMedio)
        data['medios'] = lista_medios
        return data

    def _get_hours(self, mxc):
        if mxc.intensidad == 3:
            return [mxc.hora1, mxc.hora2, mxc.hora3]
        elif mxc.intensidad == 2:
            return [mxc.hora1, mxc.hora2]
        else:
            return [mxc.hora1]

    def _update_state(self, instance):
        fechaActual = date.today()
        if instance.fechaInicio == fechaActual:
            instance.estado = estado_campania.objects.get(descripcion=1)
        elif instance.fechaInicio > fechaActual:
            instance.estado = estado_campania.objects.get(descripcion=2)
        instance.save()


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactosSerializer
    lookup_field = 'identidad'

    @action(detail=False, methods=['get'])
    def existing_groups(self, request):
        usuarias_bd = contactosxcampa.objects.values('nombreContactos').annotate(dcount=Count('nombreContactos'))
        list_nombres = [x['nombreContactos'] for x in usuarias_bd]
        return Response(list_nombres)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Medio.objects.all()
    serializer_class = MediaSerializer

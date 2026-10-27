import datetime as dt
from django.test import TestCase
from rest_framework.test import APIClient
from campaigns.models import Contacto, Campania, Operador, estado_campania, contactosxcampa, Tipo_medio, Medio, mediosxcampania, Tipo_resultado, resultadosxcampania
from campaigns.views import _cambiar_estado_bulk
from rest_framework import status

class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.estado_activo = estado_campania.objects.create(descripcion=1)
        self.operador = Operador.objects.create(email='test@test.com', clave='123')
        self.camp1 = Campania.objects.create(nombre='Camp1', fechaInicio=dt.date.today(), fechaFin=dt.date.today(), duracion=1, operador_ID=self.operador, estado=self.estado_activo)
        self.camp2 = Campania.objects.create(nombre='Camp2', fechaInicio=dt.date.today(), fechaFin=dt.date.today(), duracion=1, operador_ID=self.operador, estado=self.estado_activo)
        self.usuaria = Contacto.objects.create(identidad='123456', nombre='Test User', celular='3001234567', fecha_nacimiento=dt.date(1990,1,1), telefono='123')
        contactosxcampa.objects.create(campania=self.camp1, contacto=self.usuaria, nombreContactos='Grupo 1')
        contactosxcampa.objects.create(campania=self.camp2, contacto=self.usuaria, nombreContactos='Grupo 2')

        self.tipo_medio_wa = Tipo_medio.objects.create(descripcion=5)
        self.medio = Medio.objects.create(tipo_medio=self.tipo_medio_wa)
        mediosxcampania.objects.create(campania_id=self.camp1, medio_id=self.medio, intensidad=1)
        mediosxcampania.objects.create(campania_id=self.camp2, medio_id=self.medio, intensidad=1)

        self.tipo_resultado_orig = Tipo_resultado.objects.create(descripcion='7')
        self.tipo_resultado_new = Tipo_resultado.objects.create(descripcion='1')

        resultadosxcampania.objects.create(contacto_cc=self.usuaria, campania_id=self.camp1, medio_id=self.medio, fecha=dt.date.today(), Tipo_resultado=self.tipo_resultado_orig)
        resultadosxcampania.objects.create(contacto_cc=self.usuaria, campania_id=self.camp2, medio_id=self.medio, fecha=dt.date.today(), Tipo_resultado=self.tipo_resultado_orig)

    def test_cambiar_estado_bulk(self):
        _cambiar_estado_bulk([self.camp1, self.camp2], self.usuaria, '1')
        res1 = resultadosxcampania.objects.get(campania_id=self.camp1)
        res2 = resultadosxcampania.objects.get(campania_id=self.camp2)
        self.assertEqual(res1.Tipo_resultado, self.tipo_resultado_new)
        self.assertEqual(res2.Tipo_resultado, self.tipo_resultado_new)

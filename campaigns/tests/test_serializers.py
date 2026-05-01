import os
import django
from django.conf import settings
from django.test import TestCase
from campaigns.models import Contacto
from campaigns.serializers import ContactosSerializer
import datetime

class ContactosSerializerPerfTest(TestCase):
    def test_bulk_create_performance(self):
        data = [
            {"identidad": "1", "nombre": "Test 1", "fecha_nacimiento": "01/01/2000", "celular": "123", "telefono": "456", "email": "a@b.com"},
            {"identidad": "2", "nombre": "Test 2", "fecha_nacimiento": "02/02/2000", "celular": "123", "telefono": "456", "email": "c@d.com"}
        ]
        serializer = ContactosSerializer(data=data, many=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        contactos = serializer.save()
        self.assertEqual(len(contactos), 2)
        self.assertEqual(Contacto.objects.count(), 2)

        # Update existing and add new
        data_update = [
            {"identidad": "1", "nombre": "Test 1 Updated", "fecha_nacimiento": "01/01/2000", "celular": "123", "telefono": "456", "email": "a@b.com"},
            {"identidad": "3", "nombre": "Test 3", "fecha_nacimiento": "03/03/2000", "celular": "123", "telefono": "456", "email": "e@f.com"}
        ]
        serializer_update = ContactosSerializer(data=data_update, many=True)
        self.assertTrue(serializer_update.is_valid(), serializer_update.errors)
        contactos_update = serializer_update.save()
        self.assertEqual(len(contactos_update), 2)
        self.assertEqual(Contacto.objects.count(), 3)
        self.assertEqual(Contacto.objects.get(identidad="1").nombre, "Test 1 Updated")

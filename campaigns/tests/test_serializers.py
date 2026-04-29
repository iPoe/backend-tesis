from django.test import TestCase
from campaigns.serializers import ContactosSerializer
from campaigns.models import Contacto
import datetime

class ContactosSerializerTest(TestCase):
    def test_bulk_create_performance(self):
        data = [
            {
                'identidad': str(i),
                'nombre': f'Name {i}',
                'fecha_nacimiento': '01/01/1990',
                'celular': '1234567890',
                'telefono': '1234567890',
                'email': f'test{i}@test.com'
            }
            for i in range(10)
        ]

        serializer = ContactosSerializer(data=data, many=True)
        self.assertTrue(serializer.is_valid())

        # Test save
        contactos = serializer.save()

        self.assertEqual(len(contactos), 10)
        self.assertEqual(Contacto.objects.count(), 10)

        # Test update (conflicts)
        data[0]['nombre'] = 'Updated Name'

        serializer2 = ContactosSerializer(data=data, many=True)
        self.assertTrue(serializer2.is_valid())

        contactos2 = serializer2.save()

        self.assertEqual(len(contactos2), 10)
        self.assertEqual(Contacto.objects.count(), 10)

        c = Contacto.objects.get(identidad='0')
        self.assertEqual(c.nombre, 'Updated Name')

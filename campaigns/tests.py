from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import (
    Campania, Contacto, Medio, EmailMedio, SMSMedio, WhatsAppMedio, 
    VoiceMedio, estado_campania, Operador, Tipo_medio, CampaignTask
)
from .utils import generate_access_token
import datetime
from unittest.mock import patch

User = get_user_model()

class campaignsTests(APITestCase):
    def setUp(self):
        # Setup states
        estado_campania.objects.create(descripcion=1) # Activa
        estado_campania.objects.create(descripcion=2) # Programada
        estado_campania.objects.create(descripcion=3) # Finalizada

        # Setup media types
        self.tipo_cel = Tipo_medio.objects.create(id=1, descripcion=1)
        self.tipo_tel = Tipo_medio.objects.create(id=2, descripcion=2)
        self.tipo_email = Tipo_medio.objects.create(id=3, descripcion=3)
        self.tipo_sms = Tipo_medio.objects.create(id=4, descripcion=4)
        self.tipo_wp = Tipo_medio.objects.create(id=5, descripcion=5)
        
        # Setup operator
        self.operador = Operador.objects.create(
            email="test_op@example.com",
            clave="password123"
        )
        
        # Setup user for auth
        self.user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            clave="password123"
        )
        self.token = generate_access_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_campaign_simple(self):
        url = reverse('campaigns:campaign-list')
        data = {
            "nombre": "Test Campaign",
            "fechaInicio": "20-02-2026",
            "fechaFin": "25-02-2026",
            "duracion": 5,
            "operador_ID": self.operador.id,
            "nombreContactos": "Test Group",
            "contactos": [
                {
                    "identidad": "999999",
                    "nombre": "Test Contact",
                    "fecha_nacimiento": "01/01/1990",
                    "celular": "3000000000",
                    "email": "test@example.com",
                    "telefono": "1234567"
                }
            ],
            "medios": [
                {
                    "tipo_medio_id": 4,
                    "sms": "Hello Test",
                    "intensidad": 1,
                    "Horas": ["10:00:00"],
                }
            ]
        }
        # Note: CampaignViewSet.create uses Camp_setup which handles Contacto and Medio creation
        # We need to ensure we provide the required structure for Camp_setup
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campania.objects.count(), 1)
        self.assertEqual(CampaignTask.objects.count(), 0) # Should not create tasks if only programmed

    @patch('campaigns.twilioAPI.RestAccount.get_account_balance')
    def test_get_campaign_summary(self, mock_balance):
        mock_balance.return_value = "10.00"
        url = reverse('campaigns:campaign-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertEqual(response.data['balance'], "10.00")

    def test_create_contact(self):
        url = reverse('campaigns:contact-list')
        data = {
            "identidad": "123456",
            "nombre": "John Doe",
            "fecha_nacimiento": "01/01/1990",
            "celular": "3001234567",
            "email": "john@example.com",
            "telefono": "1234567"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contacto.objects.count(), 1)

    def test_create_email_medio(self):
        url = reverse('campaigns:media-list')
        # We need to provide a campaign ID if using the MediaSerializer logic
        # But simple creation should work too if we mock the context or just test the model aspect via serialiser
        # However, MediaSerializer.create expects campID
        camp = Campania.objects.create(
            nombre="C1",
            fechaInicio=datetime.date.today(),
            fechaFin=datetime.date.today(),
            duracion=1,
            operador_ID=self.operador,
            estado=estado_campania.objects.get(descripcion=1)
        )
        
        data = {
            "tipo_medio_id": 3,
            "email_asunt": "Subject",
            "email_cuerpo": "Body",
            "correo": "sender@example.com",
            "intensidad": 1,
            "Horas": ["09:00:00"],
            "campID": camp.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailMedio.objects.count(), 1)

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import exceptions, status
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import generate_access_token, generate_refresh_token
from django.contrib.auth.hashers import check_password
import traceback
from .models import (
    Campania, Contacto, Medio, contactosxcampa, 
    Operador, Tipo_resultado, resultadosxcampania, 
    estado_campania, Usuario
)
from .twilioAPI import WhatsApp

clientWhatsapp = WhatsApp()

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    data = request.data
    email, password = data.get('email'), data.get('clave')
    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed('email and password required')

    operador = Usuario.objects.filter(email=email).first()
    if (operador is None):
        raise exceptions.AuthenticationFailed('user not found')
    if not check_password(password, operador.clave):
        raise exceptions.AuthenticationFailed('wrong password')
    
    access_token = generate_access_token(operador)
    refresh_token = generate_refresh_token(operador)

    response = Response()
    response.set_cookie(key='refreshtoken', value=refresh_token)
    response.data = {
        'acces_token': access_token,
        'usuario': operador.id,
    }
    return response

@api_view(['POST'])
def login_operador(request):
    try:
        with transaction.atomic():
            data = request.data
            correo, password = data.get('email'), data.get('clave')
            operador = Operador.objects.filter(email=correo).first()

            if operador and password:
                if not check_password(password, operador.clave):
                    return Response({'error': 'Contraseña incorrecta'}, status=400)
                else:
                    access_token = generate_access_token(operador)
                    return Response({
                        'email': correo,
                        'id': operador.id,
                        'token': access_token
                    })
            else:
                return Response({'error': 'Correo o contraseña incorrectos'}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def save_result(request):
    try:
        with transaction.atomic():
            data = request.data
            idres = int(data['idLlamada'])
            good_status = ['completed', 'delivered', 'read']
            
            textRes = 6 if data['res'] in good_status else 7
            tipoRes = Tipo_resultado.objects.get(descripcion=textRes)
            resultadosxcampania.objects.filter(pk=idres).update(Tipo_resultado=tipoRes)
            return JsonResponse("Update completed", status=201, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@api_view(['POST'])
def reply_whatsapp(request):
    try:
        data = request.data
        wa_id = data.get('WaId', '')[2:]
        usuaria = Contacto.objects.filter(celular=wa_id).first()
        if not usuaria:
            return JsonResponse("User not found", status=404)

        campañas_usuaria = contactosxcampa.objects.filter(contacto=usuaria)
        estado_activo = estado_campania.objects.get(descripcion=1)
        campañas_activas = [c.campania for c in campañas_usuaria if c.campania.estado == estado_activo]

        if len(campañas_activas) > 0:
            mensaje_body = request.POST.get("Body", "")
            if mensaje_body == '1':
                msg = 'Gracias por querer participar'
                resultado = '1'
            elif mensaje_body == '2':
                msg = 'Entendemos que no quieras participar'
                resultado = '2'
            else:
                msg = "¡Gracias por responder!\nGracias por responder y por su interés, para mayor información, comuníquese con la E.S.E. Ladera al teléfono 8937711 Ext 0."
                resultado = '3'
            
            _cambiar_estado_bulk(campañas_activas, usuaria, resultado)
            clientWhatsapp.send_message(msg, "57" + usuaria.celular)
            
            # Resend original message if needed or confirm
            return JsonResponse("Reply completed", status=201, safe=False)
        return JsonResponse("No active campaigns", status=200)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=400)

def _cambiar_estado_bulk(campanias, usuaria, resultado):
    from datetime import date
    fechaActual = date.today()
    tipo_resultado = Tipo_resultado.objects.get(descripcion=resultado)

    for campania in campanias:
        try:
            # Find the WhatsApp media for this campaign
            from .models import mediosxcampania
            mxc = mediosxcampania.objects.filter(campania_id=campania, medio_id__tipo_medio__descripcion=5).first()
            if mxc:
                resultadosxcampania.objects.filter(
                    contacto_cc=usuaria.identidad, 
                    campania_id=campania,
                    medio_id=mxc.medio_id,
                    fecha=fechaActual
                ).update(Tipo_resultado=tipo_resultado)
        except Exception as e:
            print(f"Error updating result: {e}")

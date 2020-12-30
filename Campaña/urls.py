from django.urls import path

from . import views

app_name = 'campaña'
urlpatterns = [	
    path('camp/', views.campania_view),
    path('g_camp/', views.get_campanias),#Endpoint que de vuelve todas las campañas
    path('gu/',views.usuarias_existentes),
    path('l/',views.login_operador),
    path('sr/',views.save_result),
    path('ucamp/',views.updateCamp),
    path('fcamp/',views.endCamp),
    path('count/',views.recuento_camp),
    path('est/',views.estadisticas_campaña),
    path('pr/',views.test_estadisticas),
    




    #path('cont/',views.Agregrar_contactos,),


]
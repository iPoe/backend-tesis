from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import CampaignViewSet, ContactViewSet, MediaViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'media', MediaViewSet, basename='media')

app_name = 'campaigns'

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Webhooks & Auth
    path('whatsapp/', views.reply_whatsapp),
    path('login/', views.login_view),
    path('l/', views.login_operador),
    path('sr/', views.save_result),
]
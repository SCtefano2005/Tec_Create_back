from django.urls import path, include
from .views import  GoogleAuthView



urlpatterns = [
    path('google-auth/', GoogleAuthView.as_view(), name='google-auth'),  # Endpoint para autenticación con Google
]

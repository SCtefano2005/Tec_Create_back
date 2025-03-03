from django.urls import path
from .views import google_auth

urlpatterns = [
    path('google-auth/', google_auth, name='google_auth'),
]

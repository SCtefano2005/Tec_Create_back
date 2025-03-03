import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.text import slugify


@csrf_exempt
def google_auth(request):
    if request.method == 'POST':
        try:
            # Obtener datos en JSON desde el frontend
            data = json.loads(request.body)
            token = data.get('token')

            if not token:
                return JsonResponse({'error': 'Token no proporcionado'}, status=400)

            # Verificar el token con Google
            google_url = "https://oauth2.googleapis.com/tokeninfo"
            response = requests.get(f"{google_url}?id_token={token}")
            google_data = response.json()

            if "email" not in google_data:
                return JsonResponse({'error': 'Token inválido'}, status=400)

            email = google_data["email"]
            name = google_data.get("name", "")
            picture = google_data.get("picture", "")

            # Extraer nombre y apellido (si existen)
            name_parts = name.split()
            first_name = name_parts[0] if name_parts else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # Generar un nombre de usuario único basado en el email
            base_username = slugify(email.split('@')[0])  # Convertir a slug (ejemplo: "marcelo-stefano")
            username = base_username
            counter = 1

            # Evitar duplicados de nombre de usuario
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Buscar o crear el usuario
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # Autenticar y hacer login manualmente
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Respuesta JSON con la información del usuario
            return JsonResponse({
                'message': "Usuario creado y autenticado" if created else "Usuario autenticado correctamente",
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile_picture': picture,
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Solicitud JSON inválida'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

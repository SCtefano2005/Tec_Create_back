import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        google_token = request.data.get('token')
        if not google_token:
            return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar el token con Google
        google_url = "https://oauth2.googleapis.com/tokeninfo"
        response = requests.get(f"{google_url}?id_token={google_token}")
        google_data = response.json()

        if "email" not in google_data:
            return Response({"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)

        email = google_data["email"]
        name = google_data.get("name", "")
        picture = google_data.get("picture", "")

        # Buscar o crear el usuario
        user, created = CustomUser.objects.get_or_create(email=email, defaults={
            "username": email.split("@")[0],
            "is_google_user": True,
            "profile_picture": picture,
        })

        # Generar JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "profile_picture": user.profile_picture,
            }
        }, status=status.HTTP_200_OK)

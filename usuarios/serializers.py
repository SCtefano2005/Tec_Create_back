from rest_framework import serializers
from .models import CustomUser, UserProfile
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address']

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'profile_picture', 'is_google_user', 'profile']
        read_only_fields = ['email', 'is_google_user']  # El email y `is_google_user` vienen de Google, no se editan manualmente

    def update(self, instance, validated_data):
        """Permitir actualizar datos del usuario, pero no cambiar email ni is_google_user."""
        validated_data.pop('email', None)
        validated_data.pop('is_google_user', None)
        return super().update(instance, validated_data)


class CustomRegisterSerializer(RegisterSerializer):
    username = None  # Elimina el campo username

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['username'] = self.validated_data.get('email', '')  # Usa email como username
        return data
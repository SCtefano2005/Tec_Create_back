from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Elimina el campo username
    email = models.EmailField(unique=True)  # El email será único
    profile_picture = models.URLField(blank=True, null=True)  # URL de imagen de perfil
    is_google_user = models.BooleanField(default=False)  # Identificar si el usuario inició con Google

    USERNAME_FIELD = 'email'  # Usa email como identificador principal
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Campos requeridos al crear un superusuario

    objects = CustomUserManager()  # Asigna el UserManager personalizado

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.user.email}"



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)  # Usa get_or_create para evitar errores


class SocialAuthToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="social_token")
    provider = models.CharField(max_length=50, db_index=True)  # Índice para consultas más rápidas
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token de {self.user.email} - {self.provider}"


class LoginHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="login_history")
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # Permitir valores nulos
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_time}"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, SocialAuthToken, LoginHistory

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_google_user', 'is_staff')  # Mostrar campos relevantes
    ordering = ('email',)  # Ordenar por email
    search_fields = ('email', 'first_name', 'last_name')  # Buscar por email, nombre o apellido

    # Campos a mostrar en la edición de usuarios
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_google_user')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Campos a mostrar al agregar un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'profile_picture', 'is_google_user'),
        }),
    )

# Registrar los modelos en el panel de administración
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(SocialAuthToken)
admin.site.register(LoginHistory)
from django import forms
from .models import CustomUser, Avion, Vuelo, Comprador

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'cuit', 'perfil']

class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nombre_avion', 'cantidad_asientos', 'cantidad_filas', 'cantidad_sillas_por_fila']

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ['numero_vuelo', 'fecha_inicio', 'fecha_fin', 'avion', 'aeropuerto_origen', 'aeropuerto_destino' ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class CompradorForm(forms.ModelForm):
    class Meta:
        model = Comprador
        fields = ['nombre', 'apellido', 'documento', 'email']

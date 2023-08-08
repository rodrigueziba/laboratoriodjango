from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Avion, Vuelo, Comprador, Venta


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'cuit', 'perfil']
    list_filter = ['perfil']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'cuit', 'perfil']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Avion)
admin.site.register(Vuelo)
admin.site.register(Comprador)
admin.site.register(Venta)


# Register your models here.

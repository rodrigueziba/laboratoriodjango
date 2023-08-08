from django.db import models
from django.contrib.auth.models import AbstractUser



class Avion(models.Model):
    nombre_avion = models.CharField(max_length=100)
    cantidad_asientos = models.IntegerField()
    cantidad_filas = models.IntegerField()
    cantidad_sillas_por_fila = models.IntegerField()
    

    def total_asientos(self):
        return self.cantidad_filas * self.cantidad_sillas_por_fila
    def __str__(self):
        return self.nombre_avion

class Vuelo(models.Model):
    numero_vuelo = models.CharField(max_length=20, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    aeropuerto_origen = models.CharField(max_length=100,null=True)  
    aeropuerto_destino = models.CharField(max_length=100, null=True) 

class Comprador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    email = models.EmailField()

class Venta(models.Model):
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    comprador = models.ForeignKey(Comprador, on_delete=models.CASCADE)
    asiento = models.CharField(max_length=10)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    confirmada = models.BooleanField(default=False)

class CustomUser(AbstractUser):
    PERFILES = (
        ('admin', 'Administrador'),
        ('aerolinea', 'Aerolínea'),
        ('venta', 'Venta'),
    )
    cuit = models.CharField(max_length=20)
    perfil = models.CharField(choices=PERFILES, max_length=20)
    password_changed = models.BooleanField(default=False)  #para verificar si el usuario ha cambiado la contraseña
    avion = models.ForeignKey(Avion, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.first_name + self.last_name


    def save(self, *args, **kwargs):
        if not self.password_changed:
            self.set_password(self.cuit)  # Inicializa la contraseña con el valor de cuit
            self.password_changed = False
        super().save(*args, **kwargs)


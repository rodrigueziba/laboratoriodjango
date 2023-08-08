from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .models import CustomUser, Avion, Vuelo, Comprador, Venta
from .forms import CustomUserForm, AvionForm, VueloForm, CompradorForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import threading
import time


def vista_aerolinea_redirect(request):
    if request.user.is_authenticated:
        perfil = request.user.perfil
        if perfil == 'admin':
            return redirect('vista_administrador')
        elif perfil == 'aerolinea':
            return redirect('vista_aerolinea')
        elif perfil == 'venta':
            return redirect('vista_punto_de_venta')
        else:
            return redirect('vista_no_autorizada')
    else:
        return redirect('login')

#login/logout/signin
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            perfil = user.perfil
            if not user.password_changed:  # Verificar si la contraseña ha sido cambiada
                return redirect('cambiar_clave')  # Redirigir a la página de cambio de contraseña
            elif perfil == 'admin':
                return redirect('vista_administrador')
            elif perfil == 'aerolinea':
                return redirect('vista_aerolinea')
            elif perfil == 'venta':
                return redirect('vista_punto_de_venta')
            else:
                return redirect('vista_no_autorizada')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return render(request, 'login.html')

    return render(request, 'login.html')

def sign_in_view(request):
    if request.method == 'POST':
        # Procesar el formulario de registro y crear un nuevo usuario
        username = request.POST['username']
        password = request.POST['password']
        cuit = request.POST['cuit']
        perfil = request.POST['perfil']

        if CustomUser.objects.filter(cuit=cuit).exists():
            messages.error(request, 'El CUIT ya está registrado. Intente con otro.')
            return render(request, 'sign_in.html')

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            cuit=cuit,
            perfil=perfil
        )
        user.password_changed = False  
        user.save()
        messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'sign_in.html')

def logout_view(request):
    logout(request)
    return redirect('vista_aerolinea_redirect')  # Redirecciona a la página de inicio después del logout


# Vista de administrador
@login_required
def vista_administrador(request):
    if request.user.perfil != 'admin':
        return redirect('vista_no_autorizada')

    usuarios = CustomUser.objects.all()
    return render(request, 'vista_administrador.html', {'usuarios': usuarios})

@login_required
def listar_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = CustomUserForm()
    return render(request, 'crear_usuario.html', {'form': form})

@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'editar_usuario.html', {'form': form, 'user': user})

@login_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('listar_usuarios')
    return render(request, 'eliminar_usuario.html', {'user': user})



@login_required
def lista_vuelos(request):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    vuelos = Vuelo.objects.all()
    return render(request, 'lista_vuelos.html', {'vuelos': vuelos})

@login_required
def crear_vuelo(request):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    if request.method == 'POST':
        form = VueloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El vuelo ha sido creado exitosamente!')
            return redirect('lista_vuelos')
    else:
        form = VueloForm()

    return render(request, 'crear_vuelo.html', {'form': form})

@login_required
def editar_vuelo(request, vuelo_id):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    if request.method == 'POST':
        form = VueloForm(request.POST, instance=vuelo)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El vuelo ha sido actualizado exitosamente!')
            return redirect('lista_vuelos')
    else:
        form = VueloForm(instance=vuelo)

    return render(request, 'editar_vuelo.html', {'form': form, 'vuelo': vuelo})

@login_required
def eliminar_vuelo(request, vuelo_id):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    vuelo.delete()
    messages.success(request, '¡El vuelo ha sido eliminado exitosamente!')
    return redirect('lista_vuelos')

@login_required
def lista_aviones(request):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    aviones = Avion.objects.all()
    return render(request, 'lista_aviones.html', {'aviones': aviones})


@login_required
def cargar_avion(request):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El avión ha sido cargado exitosamente!')
            return redirect('vista_aerolinea')
    else:
        form = AvionForm()

    return render(request, 'cargar_avion.html', {'form': form})

@login_required
def cambiar_clave(request):
    if request.method == 'POST':
        nueva_clave = request.POST['nueva_clave']
        request.user.set_password(nueva_clave)
        request.user.password_changed = True  
        request.user.save()
        messages.success(request, '¡La contraseña ha sido cambiada exitosamente!')
        perfil = request.user.perfil
        if perfil == 'admin':
            return redirect('vista_administrador')
        elif perfil == 'aerolinea':
            return redirect('vista_aerolinea')
        elif perfil == 'venta':
            return redirect('vista_punto_de_venta')
        else:
            return redirect('vista_no_autorizada')

    return render(request, 'cambiar_clave.html')

# Vista de aerolínea
@login_required
def vista_aerolinea(request):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    vuelos = Vuelo.objects.filter(avion__nombre_avion=request.user.avion)
    aviones = Avion.objects.all()
    return render(request, 'vista_aerolinea.html', {'vuelos': vuelos, 'aviones': aviones})



@login_required
def cargar_vuelo(request):
    if request.method == 'POST':
        form = VueloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El vuelo ha sido cargado exitosamente!')
            return redirect('vista_aerolinea')
    else:
        form = VueloForm()

    return render(request, 'cargar_vuelo.html', {'form': form})



@login_required
def editar_avion(request, avion_id):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    avion = get_object_or_404(Avion, pk=avion_id)
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El avión ha sido actualizado exitosamente!')
            return redirect('vista_aerolinea')
    else:
        form = AvionForm(instance=avion)

    return render(request, 'editar_avion.html', {'form': form, 'avion': avion})

@login_required
def eliminar_avion(request, avion_id):
    if request.user.perfil != 'aerolinea':
        return redirect('vista_no_autorizada')

    avion = get_object_or_404(Avion, pk=avion_id)
    avion.delete()
    messages.success(request, '¡El avión ha sido eliminado exitosamente!')
    return redirect('vista_aerolinea')

# Vista punto de venta
@login_required
def vista_punto_de_venta(request):
    if request.user.perfil != 'venta':
        return redirect('vista_no_autorizada')

    if request.method == 'POST':
        fecha = request.POST['fecha']
        aeropuerto_origen = request.POST['aeropuerto_origen']
        aeropuerto_destino = request.POST['aeropuerto_destino']
        vuelos = Vuelo.objects.filter(fecha_inicio__lte=fecha, fecha_fin__gte=fecha, aeropuerto_origen=aeropuerto_origen, aeropuerto_destino=aeropuerto_destino)
        return render(request, 'buscar_vuelo.html', {'vuelos': vuelos})

    return render(request, 'buscar_vuelo.html')



def bloquear_asiento(request, vuelo_id, asiento):
 
    time.sleep(60) 
  
    return JsonResponse({'status': 'error', 'message': 'El asiento se ha liberado automáticamente porque ha pasado más de 60 segundos.'})



@login_required
def vista_punto_de_venta(request):
    # Implementar la vista principal del punto de venta aquí
    if request.user.perfil != 'venta':
        return redirect('vista_no_autorizada')

    return render(request, 'vista_punto_de_venta.html')

def buscar_vuelo(request):
    if request.method == 'POST':
        fecha = request.POST['fecha']
        aeropuerto_origen = request.POST['aeropuerto_origen']
        aeropuerto_destino = request.POST['aeropuerto_destino']
        vuelos = Vuelo.objects.filter(
            fecha_inicio__lte=fecha,
            fecha_fin__gte=fecha,
            aeropuerto_origen=aeropuerto_origen,
            aeropuerto_destino=aeropuerto_destino
        )
        return render(request, 'buscar_vuelo.html', {'vuelos': vuelos})

    return render(request, 'buscar_vuelo.html')



@login_required
def listado_ventas(request):
    if request.user.perfil != 'venta':
        return redirect('vista_no_autorizada')

    ventas = Venta.objects.filter(comprador__documento=request.user.documento)
    return render(request, 'listado_ventas.html', {'ventas': ventas})


@login_required
def cancelar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if venta.confirmada:
        return redirect('vista_no_autorizada')
    
    venta.delete()
    messages.success(request, '¡La venta ha sido cancelada exitosamente!')
    return redirect('listado_ventas')












@login_required
def datos_comprador(request, vuelo_id, asiento):
    vuelo = Vuelo.objects.get(pk=vuelo_id)
    if request.method == 'POST':
        form = CompradorForm(request.POST)
        if form.is_valid():
            comprador = form.save()
            return redirect('confirmar_venta', vuelo_id=vuelo_id, asiento=asiento, comprador_id=comprador.id)
    else:
        form = CompradorForm()

    return render(request, 'datos_comprador.html', {'vuelo': vuelo, 'asiento': asiento, 'form': form})



@login_required
def confirmar_venta(request, vuelo_id, asiento, comprador_id):
    vuelo = Vuelo.objects.get(pk=vuelo_id)
    asiento = asiento
    comprador = Comprador.objects.get(pk=comprador_id)
    
    if request.method == 'POST':
        Venta.objects.create(vuelo=vuelo, comprador=comprador, asiento=asiento)
        messages.success(request, '¡La venta ha sido realizada exitosamente! Se ha enviado un correo electrónico con los detalles del vuelo.')
        send_mail('Detalles del vuelo', f'Detalles del vuelo: {vuelo.numero_vuelo}, Asiento: {asiento}', 'noreply@tuapp.com', [comprador.email], fail_silently=False)
        return redirect('vista_punto_de_venta')

    return render(request, 'confirmar_venta.html', {'vuelo': vuelo, 'asiento': asiento, 'comprador': comprador})







def bloquear_asiento(vuelo_id, asiento):
    
    time.sleep(60)
    
@login_required
def elegir_asiento(request, vuelo_id):
    vuelo = Vuelo.objects.get(pk=vuelo_id)
    if request.method == 'POST':
        asiento = request.POST['asiento']
        t = threading.Thread(target=bloquear_asiento, args=(vuelo_id, asiento))
        t.start()
        return redirect('datos_comprador', vuelo_id=vuelo_id, asiento=asiento)
    else:
        form = CompradorForm()

    return render(request, 'elegir_asiento.html', {'vuelo': vuelo, 'form': form})



@login_required
def listado_ventas(request):
    if request.user.perfil != 'venta':
        return redirect('vista_no_autorizada')

    ventas = Venta.objects.all()
    return render(request, 'listado_ventas.html', {'ventas': ventas})

# Vista no autorizada
def vista_no_autorizada(request):
    return render(request, 'vista_no_autorizada.html')


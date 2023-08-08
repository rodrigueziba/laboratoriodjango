from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_aerolinea_redirect, name='vista_aerolinea_redirect'), 

     # URLs para login, sign in y logout
    path('login/', views.login_view, name='login'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('logout/', views.logout_view, name='logout'),

    # URLs para vistas de administrador
    path('administracion/', views.vista_administrador, name='vista_administrador'),
    path('administracion/cambiar-clave/', views.cambiar_clave, name='cambiar_clave'),
    path('administracion/listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('administracion/crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('administracion/editar-usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('administracion/eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),



    # URLs para vistas de aerolínea
    path('aerolinea/', views.vista_aerolinea, name='vista_aerolinea'),
    path('aerolinea/cargar-vuelo/', views.cargar_vuelo, name='cargar_vuelo'),
    path('aerolinea/lista-vuelos/', views.lista_vuelos, name='lista_vuelos'),
    path('aerolinea/crear-vuelo/', views.crear_vuelo, name='crear_vuelo'),
    path('aerolinea/editar-vuelo/<int:vuelo_id>/', views.editar_vuelo, name='editar_vuelo'),
    path('aerolinea/eliminar-vuelo/<int:vuelo_id>/', views.eliminar_vuelo, name='eliminar_vuelo'),

    path('aerolinea/lista-aviones/', views.lista_aviones, name='lista_aviones'),
    path('aerolinea/cargar-avion/', views.cargar_avion, name='cargar_avion'),
    path('aerolinea/editar-avion/<int:avion_id>/', views.editar_avion, name='editar_avion'),
    path('aerolinea/eliminar-avion/<int:avion_id>/', views.eliminar_avion, name='eliminar_avion'),

    

    # URLs para vistas de punto de venta
 # URLs para vistas de punto de venta
    path('punto-de-venta/', views.vista_punto_de_venta, name='vista_punto_de_venta'),
    path('punto-de-venta/buscar-vuelo/', views.buscar_vuelo, name='buscar_vuelo'),
    
    path('punto-de-venta/listado-ventas/', views.listado_ventas, name='listado_ventas'),
    
    path('punto-de-venta/elegir-asiento/<int:vuelo_id>/', views.elegir_asiento, name='elegir_asiento'),
    path('punto-de-venta/datos-comprador/<int:vuelo_id>/<str:asiento>/', views.datos_comprador, name='datos_comprador'),
    path('punto-de-venta/confirmar-venta/<int:vuelo_id>/<str:asiento>/<int:comprador_id>/', views.confirmar_venta, name='confirmar_venta'),
    path('punto-de-venta/cancelar-venta/<int:venta_id>/', views.cancelar_venta, name='cancelar_venta'),
    
    # URL para vista no autorizada
    path('no-autorizado/', views.vista_no_autorizada, name='vista_no_autorizada'),
]

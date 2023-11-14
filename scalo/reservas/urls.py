from django.urls import path
from reservas import views, reservas, predio, estadisticas,email


urlpatterns = [
    #INDEX
    path('',views.index,name='index'),

    #LOGIN
    path('login',          views.login_view,   name='login'),
    path('registrar/',      views.registrarse,  name='registro'),
    path('recuperacion/',   views.recuperar_pw, name='recuperacion'),
    path('logout/',         views.deslogearse,  name='logout'),

    #Predios
    path('predios/',         views.predios,  name='predios'),
    path('predios_deporte/', views.predios_deporte, name='predios_deporte'),
    path('predio/<int:pk>/', views.predio,  name='predio'),
    path('predio/edit/',     views.editar_predio,  name='editar_mipredio'),
    path('index',            views.editar_user,  name='editar_user'),
    path('mi_predio/edit-cancha',    predio.editar_cancha,  name='editar_cancha'),
    path('mi_predio/estadisticas',    predio.stats,  name='estadisticas'),

    #Reservas
    path('mis_reservas/',         reservas.mis_reservas,  name='mis_reservas'),
    path('mis_reservas/cancel-reserva',         reservas.cancelar_reserva,  name='cancelar_reserva'),
    path('mi_predio/',         reservas.mi_predio,  name='mi_predio'),
    path('crear_reserva/',         reservas.crear_reserva,  name='crear_reserva'),
    path('get_reserva/',         reservas.get_reserva,  name='get_reserva'),
    
    path('pre_reservar/',         reservas.pre_reservar,  name='pre_reservar'),
    path('esta_ocupado/',         reservas.esta_ocupado,  name='esta_ocupado'),

    #Cancha
    path('cancha/', views.cancha, name='cancha'),

    #mp
    path('obtener_links/', views.mercadopago_func, name='mercadopago_func'),
    path('retorno-pago/', views.retorno_pago, name='retorno_pago'),
    #path('notificacion-pago/', views.notificacion_pago, name='notificacion_pago'),

    path('envio/', email.send_mail_verificar, name='envio'),


]


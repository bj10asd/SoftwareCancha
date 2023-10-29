from django.urls import path
from reservas import views, reservas


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

    #Reservas
    path('mis_reservas/',         reservas.mis_reservas,  name='mis_reservas'),
    path('mi_predio/',         reservas.mi_predio,  name='mi_predio'),
    path('crear_reserva/',         reservas.crear_reserva,  name='crear_reserva'),
    path('get_reserva/',         reservas.get_reserva,  name='get_reserva'),

    #Cancha
    path('cancha/', views.cancha, name='cancha'),

    #mp
    path('obtener_links/', views.mercadopago_func, name='mercadopago_func'),

    #prueba
    path('prueba/', views.prueba, name='prueba'),
    path('retorno-pago/', views.retorno_pago, name='retorno_pago'),
    #path('notificacion-pago/', views.notificacion_pago, name='notificacion_pago'),

]


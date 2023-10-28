from django.urls import path
from reservas import views, reservas, predio


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
    path('mi_predio/edit-cancha',    predio.editar_cancha,  name='editar_cancha'),

    #Reservas
    path('mis_reservas/',         reservas.mis_reservas,  name='mis_reservas'),
    path('mis_reservas/cancel-reserva',         reservas.cancelar_reserva,  name='cancelar_reserva'),
    path('mi_predio/',         reservas.mi_predio,  name='mi_predio'),
    path('crear_reserva/',         reservas.crear_reserva,  name='crear_reserva'),
    path('get_reserva/',         reservas.get_reserva,  name='get_reserva'),
    

    #Cancha
    path('cancha/', views.cancha, name='cancha'),

]


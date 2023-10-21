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

    #Reservas
    path('mis_reservas/',         reservas.mis_reservas,  name='mis_reservas'),
    path('mi_predio/',         reservas.mi_predio,  name='mi_predio'),
]


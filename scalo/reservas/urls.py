from django.urls import path
from reservas import views


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
    path('predio/<int:pk>/', views.predio,  name='predio'),
]


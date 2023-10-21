from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator #Paginacion.
from django.views.generic import ListView
from datetime import datetime, timedelta

from django.http import JsonResponse  #JSon
from django.http import HttpResponse
from django.db.models import Q
import string


def mis_reservas(request):
    if request.user.is_authenticated:
        reservas_lista =Reservas.objects.all()

        # Configura la paginación con 10 elementos por página
        paginator = Paginator(reservas_lista, 10)
        # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
        pagina = request.GET.get('page') or 1
        reservas = paginator.get_page(pagina)
        return render(request, 'reservas.html', {'reservas': reservas })
    else: return redirect('index')

def mis_reservas(request):
    if request.user.is_authenticated:
        filtro_txt      = request.GET.get('filtro_txt')
        fil_select      = int(request.GET.get('fil_select') or 0)
        state_select      = int(request.GET.get('state_select') or 0)
        reservas_lista   = Reservas.objects.filter(user_id=request.user).order_by('-fecha_ini') 
        if filtro_txt is not None:
            reservas_lista = reservas_lista.filter(cancha_id__predio_id__in=Predios.objects.filter( nombre__icontains=filtro_txt)).distinct()

            #predios_lista = predios_lista.filter(nombre__icontains=filtro_txt) 
        
        if fil_select != 0:
            if fil_select is not None:
                reservas_lista = reservas_lista.filter(cancha_id__deporte_id=Deportes.objects.get(id=fil_select)).distinct()
        if state_select != 0:
            if state_select is not None:
                if state_select == 1:
                    reservas_lista= reservas_lista.filter(fecha_fin__gt=datetime.now())
                else: reservas_lista= reservas_lista.filter(fecha_fin__lt=datetime.now())
        paginator = Paginator(reservas_lista, 10)
        # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
        pagina  = request.GET.get('page') or 1
        reservas = paginator.get_page(pagina)
        return render(request, 'mis_reservas.html', {'reservas':      reservas,
                                                'deportes':     Deportes.objects.all(),
                                                'filtro_txt':   filtro_txt if filtro_txt is not None else '',
                                                'fil_select':   int(fil_select),
                                                'state_select': int(state_select),
                                                })
    else: return redirect('index')
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
import json



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
        reservas_lista   = Reservas.objects.filter(user_id=request.user) 
        if filtro_txt is not None:
            reservas_lista = reservas_lista.filter(cancha_id__predio_id__in=Predios.objects.filter( nombre__icontains=filtro_txt)).distinct()

            #predios_lista = predios_lista.filter(nombre__icontains=filtro_txt) 
        
        if fil_select != 0:
            if fil_select is not None:
                reservas_lista = reservas_lista.filter(cancha_id__deporte_id=Deportes.objects.get(id=fil_select)).distinct()
        paginator = Paginator(reservas_lista, 10)
        # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
        pagina  = request.GET.get('page') or 1
        reservas = paginator.get_page(pagina)
        return render(request, 'mis_reservas.html', {'reservas':      reservas,
                                                'deportes':     Deportes.objects.all(),
                                                'filtro_txt':   filtro_txt if filtro_txt is not None else '',
                                                'fil_select':   int(fil_select)})
    else: return redirect('index')
    
def crear_reserva(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cancha_id   = request.POST.get('cancha_id')
            fecha_ini   = request.POST.get('Fecha_ini')
            fecha_fin   = request.POST.get('Fecha_fin')
            precio   = request.POST.get('precio')
            anticipo = 0
            previous_url = request.META.get('HTTP_REFERER', '/')
            usuario = request.user

            try:
                cancha = Canchas.objects.get(pk=cancha_id)
            except Canchas.DoesNotExist:
                # Manejo de error si no se encuentra la cancha
                # Puedes redirigir o mostrar un mensaje de error aquí
                messages.error(request, 'Cancha no existente')

                return redirect(previous_url)        # Crea una instancia de Reserva con los datos
            nueva_reserva = Reservas(
                user_id=usuario,
                cancha_id=cancha,
                fecha_ini=fecha_ini,
                fecha_fin=fecha_fin,
                precio=precio,
                anticipo=anticipo
            )

            # Guarda la instancia de Reserva en la base de datos
            nueva_reserva.save()
            previous_url = request.META.get('HTTP_REFERER', '/')
            
            mensaje = f'Reserva creada desde {fecha_ini} hasta {fecha_fin} con éxito.'

            # Agregar el mensaje de éxito
            messages.success(request, mensaje)

            return redirect(previous_url)
        
    else: return redirect('index')

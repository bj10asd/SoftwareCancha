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

def mi_predio(request):
    
    if request.method == 'POST' :
        name= request.POST.get('nombre')
        precio= request.POST.get('precio')
        anticipo= request.POST.get('anticipo')
        deporte= Deportes.objects.get(id=request.POST.get('deporte_cancha'))
        imagen= request.FILES['foto_cancha']
        Canchas.objects.create(predio_id=Predios.objects.filter(user_id=request.user.id).first(),
                               deporte_id=deporte,
                               nombre=name,
                               foto=imagen,
                               precio=precio,
                               anticipo=anticipo
                               )

    predio = Predios.objects.filter(user_id=request.user.id).first()
    canchas = Canchas.objects.filter(predio_id=predio)
    deportes = Deportes.objects.all()
    dia_actual = datetime.now().strftime("%d/%m")
    hora_actual = datetime.now()

    #msotrando reservas
    reservas = Reservas.objects.filter(cancha_id__in=canchas)
    #print("contando las reservas de este predio de diferentes canchas: "+ str(reservas.count()))

    # Establece los minutos y  segundos en cero
    hora_actual = hora_actual.replace(minute=0, second=0, microsecond=0)

    # Crea una lista de horas desde la hora actual hasta la medianoche (24:00)
    horas = []
    for i in range(1, 10):
        siguiente_hora = hora_actual + timedelta(hours=i)
        horas.append(siguiente_hora)
        


    return render(request,'mi_predio.html',{'predio':      predio ,
                                        'canchas':      canchas ,
                                        'deportes':     deportes,
                                        'horas':        horas,
                                        'dia_actual':   dia_actual,
                                        'reservas':     reservas})
        
    
    
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
            
            reservas = Reservas.objects.filter(cancha_id=cancha_id, fecha_fin__gt=fecha_ini, fecha_ini__lt=fecha_fin)
            
            if reservas.count() > 0:
                mensaje = f'El horario desde {fecha_ini} hasta {fecha_fin} ,esta ocupado.'

                messages.error(request,mensaje)
            else:
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
def get_reserva(request):
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        dia_hora_reserva = request.GET.get('dia_hora_reserva')
        
        dia_hora_reserva = datetime.strptime(dia_hora_reserva, '%Y-%m-%d %H:%M')

        hora_fin = dia_hora_reserva + timedelta(hours=1)

        reserva = Reservas.objects.filter(Q(cancha_id=cancha_id) & (Q(fecha_ini=dia_hora_reserva) | Q(fecha_fin=hora_fin))).first()
        mensaje =' '
        if reserva:
            logged_in_user = request.user  # Usuario logeado
            user = reserva.user_id  # Usuario reserva
            mi_reserva=''
            if user == logged_in_user:
                mi_reserva=1
            else:mi_reserva=None
                
            user_data = {
                'id': user.id,
                'username': user.username,
                # Agrega otros campos del usuario que desees incluir
            }
            dia_hora_reserva = dia_hora_reserva
            response_data = {
                'user': user_data,
                'dia_hora_reserva': dia_hora_reserva,
                'mi_reserva':mi_reserva,
                'cancha_id':cancha_id
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                'user': None,
                'dia_hora_reserva': dia_hora_reserva,
                'mi_reserva':None,
                'cancha_id':cancha_id

            }
            return JsonResponse(response_data)

            

   
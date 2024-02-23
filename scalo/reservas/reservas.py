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
from reservas import email
from django.http import JsonResponse  #JSon
from django.http import HttpResponse
from django.db.models import Q
import string
import json



def cancelar_reserva(request):
    if request.user.is_authenticated:
        if request.method == 'POST' :
            reserva_id = request.POST.get('reserva_id')
            reserva = Reservas.objects.get(id=reserva_id)
            if request.user == reserva.user_id:
                reserva.estado = 'Cancelado'
                reserva.save()
                fecha_ini= (reserva.fecha_ini - timedelta(hours=3)).strftime('%d-%m-%Y %H:%M')
                fecha_fin= (reserva.fecha_fin - timedelta(hours=3)).strftime('%H:%M')
                mensaje = f'Reserva desde {fecha_ini} hasta {fecha_fin} en {reserva.cancha_id.predio_id} cancelada con éxito.'

                # Agregar el mensaje de éxito
                messages.success(request, mensaje)

    return redirect('mis_reservas')

def mis_reservas(request):
    
    if request.user.is_authenticated:
        filtro_txt      = request.GET.get('filtro_txt')
        fil_select      = int(request.GET.get('fil_select') or 0)
        state_select      = int(request.GET.get('state_select') or 0)
        reservas_lista   = Reservas.objects.filter(user_id=request.user).order_by('-fecha_ini') 
        print("MOSTRANDO TOTALIDAD DE RESERVAS: ",reservas_lista.count())
        if filtro_txt is not None:
            reservas_lista = reservas_lista.filter(cancha_id__predio_id__in=Predios.objects.filter( nombre__icontains=filtro_txt)).distinct()

            #predios_lista = predios_lista.filter(nombre__icontains=filtro_txt) 
        
        if fil_select != 0:
            if fil_select is not None:
                reservas_lista = reservas_lista.filter(cancha_id__deporte_id=Deportes.objects.get(id=fil_select)).distinct()
        if state_select != 0:
            if state_select is not None:
                if state_select == 1:
                    reservas_lista= reservas_lista.filter(fecha_fin__gt=datetime.now()).filter(estado="Pendiente")
                else: reservas_lista= reservas_lista.filter(fecha_fin__lt=datetime.now())
        paginator = Paginator(reservas_lista, 10)
        # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
        pagina  = request.GET.get('page') or 1
        reservas = paginator.get_page(pagina)
        return render(request,
                      'mis_reservas.html',
                      {'reservas':      reservas,
                        'deportes':     Deportes.objects.all(),
                        'filtro_txt':   filtro_txt if filtro_txt is not None else '',
                        'fil_select':   int(fil_select),
                        'state_select': int(state_select),
                      }
                     )
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
    dia_reserva=''
    dia = request.GET.get('dia_reserva')
    horas = []
    container_to_scroll  = ''

    if dia is not None :
        dia = datetime.strptime(dia, "%Y-%m-%d")
        accion = request.GET.get('accion')
        nueva_fecha =''
        if accion == 'siguiente':
            #dia = datetime.strftime("%d-%m-%Y")
            nueva_fecha = dia + timedelta(days=1)
        else:
            nueva_fecha = dia - timedelta(days=1)

        dia_reserva = nueva_fecha.strftime("%Y-%m-%d") #cambio de como se muestra la fecha
        #dia_reserva = nueva_fecha.strftime("%d-%m-%Y")
        dia_actual = datetime.now()
        for i in range(12,24):#Revisar
            siguiente_hora = datetime(nueva_fecha.year, nueva_fecha.month, nueva_fecha.day, i, 0)
            horas.append(siguiente_hora) 
        container_to_scroll  = 'contenedor_canchas'
            
    else:
        fecha_hora_actual = datetime.now()           
        # Formatea la fecha y hora en el formato deseado
        dia_reserva = fecha_hora_actual.strftime("%Y-%m-%d")
        #dia_reserva = fecha_hora_actual.strftime("%d-%m-%Y")
        hora_actual = datetime.now()


        # Establece los minutos y  segundos en cero
        hora_actual = hora_actual.replace(minute=0, second=0, microsecond=0)

        # Crea una lista de horas desde la hora actual hasta la medianoche (24:00)
        for i in range(12,24):#Revisar
            siguiente_hora = datetime(hora_actual.year, hora_actual.month, hora_actual.day, i, 0)
            horas.append(siguiente_hora)
                
        
            

    canchas = Canchas.objects.filter(predio_id=predio)
    deportes = Deportes.objects.all()
    
    
    #msotrando reservas
    reservas = Reservas.objects.filter(cancha_id__in=canchas)
    #print("contando las reservas de este predio de diferentes canchas: "+ str(reservas.count()))
    # Obtén la fecha y hora actual
    return render(request,'mi_predio.html',{'predio':      predio ,
                                        'canchas':      canchas ,
                                        'deportes':     deportes,
                                        'horas':        horas,
                                        'dia_reserva':  dia_reserva,
                                        'reservas':     reservas,
                                        'container_to_scroll': container_to_scroll,
                                        })
    
            
    
    
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
            
            reservas = Reservas.objects.filter(cancha_id=cancha_id, fecha_fin__gt=fecha_ini, fecha_ini__lt=fecha_fin).exclude(estado='Cancelado')
            
            if reservas.count() > 0:
                mensaje = f'El horario desde {fecha_ini} hasta {fecha_fin},se encuentra ocupado.'

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
                datos_send_mail = {
                    'user_name': usuario.first_name,
                    'user_telefono': '4229300',
                    'mail': usuario.email,
                    'fecha_ini': fecha_ini,
                    'fecha_fin': fecha_fin,
                    'anticipo':anticipo,
                    'precio':precio,
                    'predio_nom':cancha.predio_id.nombre,
                    'predio_tele':cancha.predio_id.telefono,
                    'predio_ubicacion':cancha.predio_id.direccion,
                    'predio_email':cancha.predio_id.email,
                    'cancha_nombre':cancha.nombre,
                    'rute': request.build_absolute_uri(),

                }
                email.send_cliente_email(datos_send_mail)
                email.send_predio_email(datos_send_mail)

                return HttpResponse ('jola')
                nueva_reserva.save()
                previous_url = request.META.get('HTTP_REFERER', '/')
                
                mensaje = f'Reserva creada desde {fecha_ini} hasta {fecha_fin} con éxito.'

                # Agregar el mensaje de éxito
                messages.success(request, mensaje)                
                

            return redirect(previous_url)
        
    else: 
        mensaje = f'Necesita estar logueado para poder reservar'
        messages.error(request,mensaje)
        previous_url = request.META.get('HTTP_REFERER', '/')

        return redirect(previous_url)
    
    
    
def get_reserva(request):
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        dia_hora_reserva = request.GET.get('dia_hora_reserva')
        
        dia_hora_reserva = datetime.strptime(dia_hora_reserva, '%Y-%m-%d %H:%M')

        hora_fin = dia_hora_reserva + timedelta(hours=1)
        
        reserva = Reservas.objects.filter(Q(cancha_id=cancha_id) & (Q(fecha_ini=dia_hora_reserva) | Q(fecha_fin=hora_fin))).exclude(estado='Cancelado').first()
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

            
def pre_reservar(request):
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        fecha_ini = request.GET.get('fecha_ini')
        f_ini = datetime.strptime(fecha_ini+":00", '%Y-%m-%d %H:%M:%S')
        reserva = Reservas.objects.filter(Q(cancha_id = int(cancha_id),fecha_ini=f_ini)).exclude(estado='Cancelado') 
                                           # & Q(estado='Activo') | Q(estado='Pendiente'))
        #print("mostrando filtro reserva ",reserva)
        if reserva.count()>0:

            response_data = {
                'disp': 'nd',
            }
            return JsonResponse(response_data)
        else:
            c = Canchas.objects.get(pk = cancha_id)
            #print(c)
            nr = Reservas()
            nr.user_id        = request.user
            nr.cancha_id      = c
            nr.fecha_ini      = f_ini
            #nr.fecha_fin     = 
            nr.precio         = c.precio
            nr.anticipo       = c.anticipo
            nr.fecha_creacion = datetime.today()
            nr.save()
            #print("pk de la nueva reserva ",nr.pk)
            response_data = {
                'disp': 'd',
                'id_r':nr.pk
            }
            return JsonResponse(response_data)

def esta_ocupado(request):
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        fecha_ini = request.GET.get('fecha_ini')
        f_ini = datetime.strptime(fecha_ini+":00", '%Y-%m-%d %H:%M:%S')
        reserva = Reservas.objects.filter(Q(cancha_id = int(cancha_id),fecha_ini=f_ini)).exclude(estado='Cancelado') 
                                           # & Q(estado='Activo') | Q(estado='Pendiente'))
        print("mostrando filtro reserva ",reserva)
        if reserva.count()>0:
            response_data = {
                'disp': 'nd',
            }
            #return JsonResponse(response_data)
        else:
            response_data = {
                'disp': 'd',
            }
        return JsonResponse(response_data)
   
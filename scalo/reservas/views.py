from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas,usuarios
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator #Paginacion.
from django.views.generic import ListView
from datetime import datetime, timedelta,date

from django.http import JsonResponse  #JSon
from django.http import HttpResponse
from django.db.models import Q
import string
import json

# Create your views here.

#def hello(request):
#    return render(request,'hello.html',{})

def index(request):
    #cancha = Cancha.objects.all()
    return render(request,'index.html',{})#,{'canchas':cancha})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        print("Pag anterior")
        print(request.POST.get('ant'))
        print(request.POST.get('ant').split('/'))
        print(request.POST.get('ant').split('/')[-2])
        ant = request.POST.get('ant').split('/')
        user = request.POST.get('email').split("@")[0]
        pw   = request.POST.get('password')
        us = authenticate(username=user,password=pw)#authenticate solo si existe o no en la bd
        if us:
            login(request,us)
            messages.success(request, 'Bienvenido {}'.format(us.email))
            print('Bienvenido {}'.format(us.get_username()))
            if ant[-3] == 'predio':
                return redirect('predio', pk=(request.POST.get('ant').split('/')[-2]))
            else:
                return redirect('predios')
        else:
            messages.error(request, "Usuario o contraseña invalidos")
            return redirect('login')

    return render(request, 'auth/login.html',{})

def deslogearse(request):
    logout(request)
    return redirect('index')

def registrarse(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        e   = request.POST.get('email')
        rdo = User.objects.filter(email=e).count()
        if rdo > 0:
            messages.error(request, 'El email proporcionado ya está en uso')
            return redirect('registro')
        else:
            p1 = request.POST.get('password')
            p2 = request.POST.get('password2')
            if p1!=p2:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('registro')
            else:
                if len(p1)<7:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                    return redirect('registro')
                else:
                    if not any(c.isupper() for c in p1):
                        messages.error(request, 'La contraseña debe contener una mayuscula')
                        return redirect('registro')
                    if not any(c in string.punctuation for c in p1):
                        #C: !" #$%&'()*+,-./:;<=>?@[\]^_`{|} ~.
                        messages.error(request, 'La contraseña debe contener al menos un caracter especial')
                        return redirect('registro')
            #AL NO PEDIR USUARIO, VAMOS A GENERAR EL USUARIO APARTIR DEL EMAIL
            #ES DECIR EL USUARIO SERA LO QUE ANTECEDA AL @
            u = request.POST.get('email').split("@")[0]
            user = User.objects.create_user(u,e,request.POST.get('password'))
            
            if user:
                user.first_name = request.POST.get('nombre')
                user.last_name  = request.POST.get('apellido')
                extra_fields(user,request.POST.get('fec_nac'),request.POST.get('telef'))
                DarRol(user,"Cliente")
                login(request,user)
                p= Permission.objects.get(name='Can view Reserva')
                user.user_permissions.add(p)
                user.save()
                messages.success(request, 'Usuario registrado exitosamente, bienvenido {}'.format(user.email))
                return redirect('predios')
            else:
                print('Ocurrió un error')    
    return render(request,'auth/registrarse.html',{})

def DarRol(user,rol):
    nuevo_ru = UsuarioXRoles()
    nuevo_ru.user_id = user
    nuevo_ru.rol_id  = Roles.objects.get(descripcion=rol)
    nuevo_ru.save()

def extra_fields(user,fec_nac,telef):
    u = usuarios()
    u.user_id = user
    u.fec_nac = fec_nac
    u.telef   = telef
    u.save()


def recuperar_pw(request):
    return render(request,'auth/recuperacion_pw.html',{})


def predios(request):
    filtro_txt      = request.GET.get('filtro_txt')
    fil_select      = int(request.GET.get('fil_select') or 0)
    predios_lista   = Predios.objects.all() 
    if filtro_txt is not None:
        predios_lista = predios_lista.filter(canchas__isnull=False, nombre__icontains=filtro_txt).distinct()

        #predios_lista = predios_lista.filter(nombre__icontains=filtro_txt) 
    
    if fil_select != 0:
        if fil_select is not None:
            predios_lista = predios_lista.filter(id__in=Canchas.objects.filter(deporte_id=fil_select).values('predio_id')).distinct()
            
    paginator = Paginator(predios_lista, 10)
    # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
    pagina  = request.GET.get('page') or 1
    predios = paginator.get_page(pagina)
    return render(request, 'predios.html', {'predios':      predios,
                                            'deportes':     Deportes.objects.all(),
                                            'filtro_txt':   filtro_txt if filtro_txt is not None else '',
                                            'fil_select':   int(fil_select)})

def predio(request,pk):#import datetime
    if request.method == 'GET':
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
            if nueva_fecha.year == dia_actual.year and nueva_fecha.month == nueva_fecha.month and dia.day == nueva_fecha.day:

                fecha_hora_actual = datetime.now()           
                #dia_reserva = fecha_hora_actual.strftime("%d-%m-%Y")
                hora_actual = datetime.now()


                # Establece los minutos y  segundos en cero
                hora_actual = hora_actual.replace(minute=0, second=0, microsecond=0)

                # Crea una lista de horas desde la hora actual hasta la medianoche (24:00)
                for i in range(1, 10):
                    siguiente_hora = hora_actual + timedelta(hours=i)
                    if siguiente_hora.hour <= 23 and siguiente_hora.hour !=0  :
                        horas.append(siguiente_hora)
                    else:
                        break
            else:
                           
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
            for i in range(1, 10):
                siguiente_hora = hora_actual + timedelta(hours=i)
                if siguiente_hora.hour <= 23 and siguiente_hora.hour !=0  :
                    horas.append(siguiente_hora)
                else:
                    break
                

        predio = Predios.objects.get(id=pk)
        canchas = Canchas.objects.filter(predio_id=predio)
        deportes = Deportes.objects.all()
        
        
        #msotrando reservas
        reservas = Reservas.objects.filter(cancha_id__in=canchas)
        #print("contando las reservas de este predio de diferentes canchas: "+ str(reservas.count()))
        # Obtén la fecha y hora actual

        return render(request,'predio.html',{'predio':      predio ,
                                            'canchas':      canchas ,
                                            'deportes':     deportes,
                                            'horas':        horas,
                                            'dia_reserva':  dia_reserva,
                                            'reservas':     reservas,
                                            'container_to_scroll': container_to_scroll,
                                            })
        

def predios_deporte(request):
    if request.method == 'GET':

        deporte_id = request.GET.get('deporte_id')
        predio_id = request.GET.get('predio_id')

        #return HttpResponse(deporte_id, content_type='text/plain')
        canchas_data=[]
        if(deporte_id!='all'):
            deporte = Deportes.objects.filter(id=deporte_id).first()

            canchas = Canchas.objects.filter(Q(predio_id=predio_id) & Q(deporte_id=deporte_id))

            for cancha in canchas:
                canchas_data.append({
                    'cancha_id':cancha.id,
                    'predio_id': cancha.predio_id.nombre,
                    'deporte': cancha.deporte_id.descripcion,
                    'nombre': cancha.nombre,
                    'foto': cancha.foto.url,  # URL de la imagen
                    'precio': cancha.precio,
                    'anticipo': cancha.anticipo,
                })
        else:
            canchas = Canchas.objects.filter(predio_id=predio_id)
            for cancha in canchas:
                canchas_data.append({
                    'cancha_id':cancha.id,
                    'predio_id': cancha.predio_id.nombre,
                    'deporte': cancha.deporte_id.descripcion,
                    'nombre': cancha.nombre,
                    'foto': cancha.foto.url,  # URL de la imagen
                    'precio': cancha.precio,
                    'anticipo': cancha.anticipo,
                })

        return JsonResponse(canchas_data, safe=False)
    
def cancha(request):
    cancha_data = ''
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        cancha = Canchas.objects.filter(id=cancha_id).first()
        cancha_data = {
                'id': cancha.id,
                'nombre': cancha.nombre,
                'precio': cancha.precio,
            }

    return JsonResponse(cancha_data, safe=False)


def editar_predio(request):
    print(request.POST.get('predio_id'))
    print(request.POST.get('predio'))
    print(request.POST.get('direccion'))
    print(request.POST.get('telef'))
    print(request.POST.get('mapa'))
    print(request.POST.get('descripcion'))
    p = Predios.objects.get(id=request.POST.get('predio_id'))
    p.direccion   = request.POST.get('direccion')   if request.POST.get('direccion') is not None else p.direccion
    p.nombre      = request.POST.get('predio')      if request.POST.get('predio') is not None else p.nombre
    p.telefono    = request.POST.get('telef')       if request.POST.get('telef') is not None else p.telefono
    p.link_mapa   = request.POST.get('mapa')        if request.POST.get('mapa') is not None else p.link_mapa
    p.descripcion = request.POST.get('descripcion') if request.POST.get('descripcion') is not None else p.descripcion
    p.save()
    return redirect('mi_predio')
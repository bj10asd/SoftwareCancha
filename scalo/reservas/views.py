from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas
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
                DarRol(user,"Cliente")
                login(request,user)
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

def recuperar_pw(request):
    return render(request,'auth/recuperacion_pw.html',{})

def predios(request):
    predios_lista =Predios.objects.all()

    # Configura la paginación con 10 elementos por página
    paginator = Paginator(predios_lista, 10)
    # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
    pagina = request.GET.get('page') or 1
    predios = paginator.get_page(pagina)
    return render(request, 'predios.html', {'predios': predios })

def predios(request):
    predios_lista =Predios.objects.all()

    # Configura la paginación con 10 elementos por página
    paginator = Paginator(predios_lista, 10)
    # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
    pagina = request.GET.get('page') or 1
    predios = paginator.get_page(pagina)
    return render(request, 'predios.html', {'predios': predios })

def predio(request,pk):#import datetime
    
    predio = Predios.objects.get(id=pk)
    canchas = Canchas.objects.filter(predio_id=predio)
    deportes = Deportes.objects.all()
    dia_actual = datetime.now().strftime("%d/%m")
    hora_actual = datetime.now()

    # Establece los minutos y  segundos en cero
    hora_actual = hora_actual.replace(minute=0, second=0, microsecond=0)

    # Crea una lista de horas desde la hora actual hasta la medianoche (24:00)
    horas = []
    for i in range(1, 10):
        siguiente_hora = hora_actual + timedelta(hours=i)
        horas.append(siguiente_hora)
        


    return render(request,'predio.html',{'predio':predio ,'canchas':canchas ,'deportes':deportes,'horas':horas,'dia_actual':dia_actual})
        

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
            canchas = Canchas.objects.all()
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

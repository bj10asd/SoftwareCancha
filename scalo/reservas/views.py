from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import UsuarioXRoles,Roles,Predios
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
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
        #print(request.POST.get('ant').split('/')[-2])
        #user = request.POST.get('username')
        ant = request.POST.get('ant').split('/')[-2]
        user = request.POST.get('email').split("@")[0]
        pw   = request.POST.get('password')
        us = authenticate(username=user,password=pw)#authenticate solo si existe o no en la bd
        if us:
            login(request,us)
            messages.success(request, 'Bienvenido {}'.format(us.first_name)+' '+format(us.last_name))
            print('Bienvenido {}'.format(us.get_username()))
            if ant is None or ant == 'predios':
                return redirect('predios')
            else:
                return redirect('predio', pk=(request.POST.get('ant').split('/')[-2]))
        else:
            messages.error(request, "Usuario o contraseña invalidos")
            return redirect('auth/login')

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
            return redirect('auth/registro')
        else:
            p1 = request.POST.get('password')
            p2 = request.POST.get('password2')
            if p1!=p2:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('auth/registro')
            else:
                if len(p1)<7:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                    return redirect('auth/registro')
                else:
                    if not any(c.isupper() for c in p1):
                        messages.error(request, 'La contraseña debe contener una mayuscula')
                        return redirect('auth/registro')
                    if not any(c in string.punctuation for c in p1):
                        #C: !" #$%&'()*+,-./:;<=>?@[\]^_`{|} ~.
                        messages.error(request, 'La contraseña debe contener al menos un caracter especial')
                        return redirect('auth/registro')
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
    p = Predios.objects.all()
    return render(request,'predios.html',{'p':p})

def predio(request,pk):
    p = Predios.objects.get(id=pk)
    return render(request,'predio.html',{'p':p})
        
    
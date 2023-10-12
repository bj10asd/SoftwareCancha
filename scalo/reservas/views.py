from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import Canchas,UsuarioXRoles,Roles,Reservas
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# Create your views here.

#def hello(request):
#    return render(request,'hello.html',{})

def index(request):
    #cancha = Cancha.objects.all()
    return render(request,'index.html',{})#,{'canchas':cancha})

def login_view(request):
    #pass
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        user = request.POST.get('username')
        pw   = request.POST.get('password')
        us = authenticate(username=user,password=pw)#authenticate solo si existe o no en la bd
        if us:
            login(request,us)
            messages.success(request, 'Bienvenido {}'.format(us.first_name)+' '+format(us.last_name))
            print('Bienvenido {}'.format(us.get_username()))
            return redirect('index')
        else:
            messages.error(request, "Usuario o contraseña invalidos")
            return redirect('login')

    return render(request, 'login.html',{})

def deslogearse(request):
    logout(request)
    return redirect('index')

def registrarse(request):
    #pass
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        e = request.POST.get('email')
        rdo = User.objects.filter(email=e).count()
        if rdo > 0:
            messages.error(request, 'El email proporcionado ya está en uso')
            return redirect('registro')
        else:
            u = request.POST.get('username')
            p = request.POST.get('password')
            user = User.objects.create_user(u,e,p)
            
            if user:
                if request.POST.get('switch') == 'on':
                    #print("QUIERE SER CANCHERO")
                    DarRol(user,'Canchero')
                else:
                    #print('QUIERE JUGAR A LA PELOTA')
                    DarRol(user,"Jugador")
                user.first_name = request.POST.get('nombre')
                user.last_name  = request.POST.get('apellido') or ''
                user.save() 
                login(request,user)
                messages.success(request, 'Registro completo, bienvenido {}'.format(user.first_name)+' '+format(user.last_name))
                return redirect('index')
            else:
                print('nose pudo')
    return render(request,'registro.html',{})

def DarRol(user,rol):
    nuevo_ru = UsuarioXRoles()
    nuevo_ru.user_id = user
    nuevo_ru.rol_id  = Roles.objects.get(descripcion=rol)
    nuevo_ru.save()
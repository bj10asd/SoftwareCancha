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


def editar_cancha(request):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST' :
                cancha=Canchas.objects.get(id= request.POST.get('cancha_id'))
                if Predios.objects.filter(user_id=request.user).first()==cancha.predio_id:
                    name= request.POST.get('nombre')
                    precio= request.POST.get('precio')
                    anticipo= request.POST.get('anticipo')
                    if len(request.FILES) != 0:
                        imagen= request.FILES['foto_cancha']
                        cancha.foto.delete()
                        cancha.foto=imagen
                    cancha.nombre=name
                    cancha.precio=precio
                    cancha.anticipo=anticipo
                    cancha.save()
                    messages.success(request, f'{cancha.nombre} modificada correctamente.')
    except Exception:
        messages.error(request, 'Error al modificar cancha.')
            
    return redirect('mi_predio')
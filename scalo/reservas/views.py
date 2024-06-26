from django.shortcuts import render, get_object_or_404, redirect
from django.urls import path
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas,usuarios,pagos
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator #Paginacion.
from django.views.generic import ListView
from datetime import datetime, timedelta,date
from django.conf import settings
from django.http import JsonResponse  #JSon
from django.http import HttpResponse
from django.db.models import Q
import string
import json
from django.urls import reverse
from reservas import email
import os


#at=APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137

# Create your views here.

#def hello(request):
#    return render(request,'hello.html',{})
ngrok_url = settings.NGROK_URL

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
        #print(perfil_usuario)
        if us:
            login(request,us)
            messages.success(request, 'Bienvenido {}'.format(us.email))
            print('Bienvenido {}'.format(us.get_username()))
            if ant[-3] == 'predio':
                return redirect('predio', pk=(request.POST.get('ant').split('/')[-2]))
            else:
                return redirect('predios')
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
            return redirect('login')

    return render(request, 'auth/login.html',{})

def deslogearse(request):
    logout(request)
    return redirect('index')

def es_menor(fec_nac):
    #year=fec_nac.year
    #month = fec_nac.month
    #day = fec_nac.day
    #date = date(year,month,day)
    now = date.today()
    return (
        now.year - fec_nac.year < 18
        or now.year - fec_nac.year == 18 and (
            now.month < fec_nac.month 
            or now.month == fec_nac.month and now.day <= fec_nac.day
        )
    )

def registrarse(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        e   = request.POST.get('email')
        rdo = User.objects.filter(email=e).count()
        if rdo > 0:
            messages.error(request, 'El email proporcionado ya está en uso.')
            return redirect('registro')
        elif datetime.strptime(request.POST.get('fec_nac'),'%Y-%m-%d')>=datetime.now():
            messages.error(request, 'La fecha proporcionada no puede ser mayor a hoy.')
            return redirect('registro')
        elif es_menor(datetime.strptime(request.POST.get('fec_nac'),'%Y-%m-%d')):
            print(datetime.now()-datetime.strptime(request.POST.get('fec_nac'),'%Y-%m-%d'))
            messages.error(request, 'La persona no es mayor de 18 años.')
            return redirect('registro')
        elif datetime.strptime(request.POST.get('fec_nac'),'%Y-%m-%d').year<=1900:
            #print(datetime.now()-datetime.strptime(request.POST.get('fec_nac'),'%Y-%m-%d'))
            messages.error(request, 'El año debe ser mayor a 1900.')
            return redirect('registro')
        else:
            p1 = request.POST.get('password')
            p2 = request.POST.get('password2')
            if p1!=p2:
                messages.error(request, 'Las contraseñas no coinciden.')
                return redirect('registro')
            else:
                if len(p1)<7:
                    messages.error(request, 'La contraseña debe tener al menos 8 carácteres.')
                    return redirect('registro')
                else:
                    if not any(c.isupper() for c in p1):
                        messages.error(request, 'La contraseña debe contener una mayúscula.')
                        return redirect('registro')
                    if not any(c in string.punctuation for c in p1):
                        #C: !" #$%&'()*+,-./:;<=>?@[\]^_`{|} ~.
                        messages.error(request, 'La contraseña debe contener al menos un carácter especial')
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
                print('Ocurrió un error.')    
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

import requests
import json
def consulta_api(klave):
    url = "https://5jt.000webhostapp.com/get_photos.php"

    # Datos que deseas enviar en la solicitud POST
    data_to_send = {
        #'klave': 'estelaevelia.herrera@gmail.com'
        'klave': klave
    }

    try:
        # Realizar la solicitud POST
        #headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data_to_send))#,headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            #print("mostrando dict: ",json_data.get('resultado'))
            return json_data.get('resultado')

        else:
            # Manejar el caso en el que la solicitud no fue exitosa
            #return JsonResponse({'error': 'Error en la solicitud'}, status=500)
            return "Hubo un error1"

    except requests.RequestException as e:
        # Manejar excepciones de la biblioteca requests
        #return JsonResponse({'error': f'Error en la solicitud: {str(e)}'}, status=500)
        return "Hubo un error2"

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
            
    rta = []
    for e in predios_lista:
        #Nueva forma de obtener imagenes:
        #print("pidiendo los datos del predio: ",e.user_id.username+"_p")
        klave = e.user_id.username+"_p"
        rta.append({
            'id'        : Predios.objects.get(user_id = e.user_id).pk,#e.user_id.pk,
            'logo'      : consulta_api(klave),
            'link_mapa' : e.link_mapa,
            'direccion' : e.direccion,
            'nombre'    : e.nombre,
        })

    #print("mostrando rta: ",rta)

    #paginator = Paginator(predios_lista, 10)
    paginator = Paginator(rta, 10)
    # Obtiene el número de página de la URL o utiliza la página 1 como predeterminada
    pagina  = request.GET.get('page') or 1
    predios = paginator.get_page(pagina)
    return render(request, 'predios.html', {'predios':      predios,
                                            'deportes':     Deportes.objects.all(),
                                            'filtro_txt':   filtro_txt if filtro_txt is not None else '',
                                            'fil_select':   int(fil_select)})

def predio(request,pk):#import datetime
    predio = Predios.objects.get(id=pk)
    p_hora_fin = ''
    p_hora_inicio=''
    if predio.hora_fin is None:
         p_hora_fin = 24
    else:
        p_hora_fin = int(predio.hora_fin)
    if predio.hora_ini is None:
        p_hora_inicio= 12
    else:
        p_hora_inicio = int(predio.hora_ini)
    #return HttpResponse(p_hora_inicio)
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
            if nueva_fecha.year == dia_actual.year and nueva_fecha.month == dia_actual.month and nueva_fecha.day == dia_actual.day:

                fecha_hora_actual = datetime.now()           
                #dia_reserva = fecha_hora_actual.strftime("%d-%m-%Y")
                hora_actual = datetime.now()


                # Establece los minutos y  segundos en cero
                hora_actual = hora_actual.replace(minute=0, second=0, microsecond=0)

                siguiente_hora = hora_actual + timedelta(hours=1)
                while(siguiente_hora.hour < p_hora_inicio):
                    siguiente_hora = siguiente_hora + timedelta(hours=1)
                    
                for i in range(1, 24):
                    if siguiente_hora.hour < p_hora_fin and siguiente_hora.hour >= p_hora_inicio:
                        horas.append(siguiente_hora)
                        siguiente_hora = siguiente_hora + timedelta(hours=1)
                    else:
                        break
            else:                          
                for i in range(p_hora_inicio,p_hora_fin):#Revisar
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
            siguiente_hora = hora_actual + timedelta(hours=1)
            while(siguiente_hora.hour < p_hora_inicio):
                
                siguiente_hora = siguiente_hora + timedelta(hours=1)
                
            for i in range(1, 24):
                if siguiente_hora.hour < p_hora_fin and siguiente_hora.hour >= p_hora_inicio:
                    horas.append(siguiente_hora)
                    siguiente_hora = siguiente_hora + timedelta(hours=1)
                else:
                    break
                    
                

        canchas = Canchas.objects.filter(predio_id=predio)

        #Nuevo metodo de mostrar imagenes
        c = []
        for e in canchas:
            klave = e.predio_id.user_id.username+"_c_"+str(e.pk)
            c.append({
                'id'         : e.id,
                'predio_id'  : e.predio_id,
                'deporte_id' : e.deporte_id,
                'nombre'     : e.nombre,
                'foto'       : consulta_api(klave),
                'precio'     : e.precio,
                'anticipo'   : e.anticipo,
            })

        deportes = Deportes.objects.all()
        #msotrando reservas
        reservas = Reservas.objects.filter(cancha_id__in=canchas).exclude(estado='Cancelado')
        #print("contando las reservas de este predio de diferentes canchas: "+ str(reservas.count()))
        # Obtén la fecha y hora actual

        return render(request,'predio.html',{'predio':      predio ,
                                            #'canchas':      canchas ,
                                            'canchas':      c ,
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
                klave = cancha.predio_id.user_id.username+"_c_"+str(cancha.pk)
                canchas_data.append({
                    'cancha_id':cancha.id,
                    'predio_id': cancha.predio_id.nombre,
                    'deporte': cancha.deporte_id.descripcion,
                    'nombre': cancha.nombre,
                    #'foto': cancha.foto.url,  # URL de la imagen
                    'foto': consulta_api(klave),
                    'precio': cancha.precio,
                    'anticipo': cancha.anticipo,
                })
        else:
            canchas = Canchas.objects.filter(predio_id=predio_id)

            for cancha in canchas:
                klave = cancha.predio_id.user_id.username+"_c_"+str(cancha.pk)
                canchas_data.append({
                    'cancha_id':cancha.id,
                    'predio_id': cancha.predio_id.nombre,
                    'deporte': cancha.deporte_id.descripcion,
                    'nombre': cancha.nombre,
                    #'foto': cancha.foto.url,  # URL de la imagen
                    'foto': consulta_api(klave),
                    'precio': cancha.precio,
                    'anticipo': cancha.anticipo,
                })

        return JsonResponse(canchas_data, safe=False)

def filtrar_fotoslider(request):#Fotos Slider


    if request.method == 'GET':

        #deporte_id = request.GET.get('deporte_id')
        #predio_id = request.GET.get('predio_id')
        cancha_id = int(request.GET.get('cancha_id')) if request.GET.get('cancha_id') else 0
        #print
        #return HttpResponse(deporte_id, content_type='text/plain')
        canchas_data=[]
        #if(deporte_id!='all'):
            #deporte = Deportes.objects.filter(id=deporte_id).first()

        #canchas = Canchas.objects.filter(Q(predio_id=predio_id) & Q(deporte_id=deporte_id))
        canchas = Canchas.objects.filter(pk=cancha_id)
        for cancha in canchas:
            klave = cancha.predio_id.user_id.username+"_c_"+str(cancha.pk)
            canchas_data.append({
                'cancha_id':cancha.id,
                'predio_id': cancha.predio_id.nombre,
                'deporte': cancha.deporte_id.descripcion,
                'nombre': cancha.nombre,
                #'foto': cancha.foto.url,  # URL de la imagen
                'foto': consulta_api(klave),
                'precio': cancha.precio,
                'anticipo': cancha.anticipo,
            })
        """else:
            canchas = Canchas.objects.filter(predio_id=predio_id)

            for cancha in canchas:
                klave = cancha.predio_id.user_id.username+"_c_"+str(cancha.pk)
                canchas_data.append({
                    'cancha_id':cancha.id,
                    'predio_id': cancha.predio_id.nombre,
                    'deporte': cancha.deporte_id.descripcion,
                    'nombre': cancha.nombre,
                    #'foto': cancha.foto.url,  # URL de la imagen
                    'foto': consulta_api(klave),
                    'precio': cancha.precio,
                    'anticipo': cancha.anticipo,
                })
        """
        print("canchas devuelta: ",canchas_data)
        return JsonResponse(canchas_data, safe=False)
    
import mercadopago    
def cancha(request):
    cancha_data = ''
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        cancha = Canchas.objects.filter(id=cancha_id).first()
        

        # Agrega credenciales
        #sdk = mercadopago.SDK("APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137")
        
        # Crea un ítem en la preferencia
        """preference_data = {
            "items": [
                {
                    "title": "Reserva",
                    "quantity": 1,
                    "currency_id":"ARS",
                    "unit_price": cancha.precio,#debería ser monto pasado por 
                }
            ],
            ""back_urls": [
                {
                    "success": "https://127.0.0.1:8000",
                    "failure": "https://127.0.0.1:8000",
                    "pending": "https://127.0.0.1:8000",                                  
                },
            ],"
            "auto_return": "approved",
        }
        preference_data_min = {
            "items": [
                {
                    "title": "Reserva",
                    "quantity": 1,
                    "currency_id":"ARS",
                    "unit_price": cancha.anticipo,#debería ser monto pasado por 
                }
            ],
            "back_urls": [
                {
                    "success": "https://2321-190-193-23-165.ngrok-free.app/prueba",                        
                },
            ],
            "auto_return": "approved",
            "notification_url":"https://2321-190-193-23-165.ngrok-free.app/prueba"

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        preference_response_min = sdk.preference().create(preference_data_min)
        preference_min = preference_response_min["response"]"""

        #print(preference)
        #print(preference['init_point'])


        cancha_data = {
                'id'       : cancha.id,
                'nombre'   : cancha.nombre,
                'precio'   : cancha.precio,
                'anticipo' : cancha.anticipo,
                #'link'     : preference['id'],
                #'p' : preference,
                #'p_min' :preference_min
            }
    return JsonResponse(cancha_data, safe=False)


def editar_predio(request):
    if len(request.POST.get('descripcion'))<100:
        print(request.POST.get('predio_id'))
        print(request.POST.get('predio'))
        print(request.POST.get('direccion'))
        print(request.POST.get('telef'))
        print(request.POST.get('mapa'))
        print(request.POST.get('descripcion'))
        print(request.POST.get('email_contacto'))
        p = Predios.objects.get(id=request.POST.get('predio_id'))
        p.direccion   = request.POST.get('direccion')   if request.POST.get('direccion') is not None else p.direccion
        p.nombre      = request.POST.get('predio')      if request.POST.get('predio') is not None else p.nombre
        p.telefono    = request.POST.get('telef')       if request.POST.get('telef') is not None else p.telefono
        p.link_mapa   = request.POST.get('mapa')        if request.POST.get('mapa') is not None else p.link_mapa
        p.descripcion = request.POST.get('descripcion') if request.POST.get('descripcion') is not None else p.descripcion
        p.email       = request.POST.get('email_contacto') if request.POST.get('email_contacto') is not None else p.email
        p.hora_ini    = request.POST.get('hora_ini')    if request.POST.get('hora_ini') is not None else p.hora_ini
        p.hora_fin    = request.POST.get('hora_fin')   if request.POST.get('hora_fin') is not None else p.hora_fin 
        p.save()
        return redirect('mi_predio')
    else:
        messages.error(request, 'La descripción es muy grande')
        return redirect('mi_predio')
    
def editar_user(request):
    print(request.POST.get('user_id'))
    print(request.POST.get('nombre'))
    print(request.POST.get('apellido'))
    print(request.POST.get('email_user'))
    p = User.objects.get(id=request.POST.get('user_id'))
    ptel = usuarios.objects.get(user_id = request.user)
    p.first_name = request.POST.get('nombre')        if request.POST.get('nombre')        is not None else p.first_name
    p.last_name  = request.POST.get('apellido')      if request.POST.get('apellido')      is not None else p.last_name
    ptel.telef   = request.POST.get('telefono_user') if request.POST.get('telefono_user') is not None else ptel.telef
    p.email      = request.POST.get('email_user')    if request.POST.get('email_user')    is not None else p.email
    p.save()
    ptel.save()
    messages.success(request, 'Datos modificados correctamente')
    return redirect(request.META.get('HTTP_REFERER', '/'))

import mercadopago
def mercadopago_func(request):
    if request.method == 'GET':
        cancha_id = request.GET.get('cancha_id')
        cancha = Canchas.objects.filter(id=cancha_id).first()

        url = ""

        # Agrega credenciales
        sdk = mercadopago.SDK("APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137")
        
        #obteniendo la url:
        RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if RENDER_EXTERNAL_HOSTNAME:
            url = RENDER_EXTERNAL_HOSTNAME

        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "Pago de reserva en "+cancha.nombre+" "+cancha.predio_id.nombre+" Reserva Total",
                    "quantity": 1,
                    "currency_id":"ARS",
                    "unit_price": cancha.precio if int(request.GET.get('duracion')) == 60 else cancha.precio*2,
                    "description":"Pago de la totalidad"
                }
            ],
            "metadata": {
                "cancha_id": cancha_id,
                "duracion": request.GET.get('duracion'),
                "fecha_ini": request.GET.get('fecha_ini'),
                "fecha_fin": request.GET.get('fecha_fin'),
                "precio_cancha":cancha.precio if int(request.GET.get('duracion')) == 60 else cancha.precio*2
                # Agregar más campos según tus necesidades
            },
            "back_urls": {
                #"success": settings.NGROK_URL + '/retorno-pago/',
                #"failure": settings.NGROK_URL + '/retorno-pago/',
                "success": url + '/retorno-pago/',
                "failure": url + '/retorno-pago/',
            },
            "auto_return": "approved",
            #"statement_descriptor":"Reserva total.",
            #"notification_url":"https://9084-2803-9800-b402-7ed6-ba3f-4184-fa5a-474e.ngrok-free.app/notificacion-pago/",
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        preference_data_min = {
            "items": [
                {
                    "title": "Pago de anticipo reserva en "+cancha.nombre+" "+cancha.predio_id.nombre+" Reserva Total",
                    "quantity": 1,
                    "currency_id":"ARS",
                    "unit_price": cancha.anticipo if int(request.GET.get('duracion')) == 60 else cancha.anticipo*2,
                    "description":"Pago del anticipo"
                }
            ],
            "metadata": {
                "cancha_id": cancha_id,
                "duracion": request.GET.get('duracion'),
                "fecha_ini": request.GET.get('fecha_ini'),
                "fecha_fin": request.GET.get('fecha_fin'),
                "precio_cancha":cancha.precio if int(request.GET.get('duracion')) == 60 else cancha.precio*2
            },
            "back_urls": {
                #"success": settings.NGROK_URL + '/retorno-pago/',
                #"failure": settings.NGROK_URL + '/retorno-pago/',
                "success": url + '/retorno-pago/',
                "failure": url + '/retorno-pago/',
            },
            "auto_return": "approved",
            #"statement_descriptor":"Reserva total.",
        }

        preference_response_min = sdk.preference().create(preference_data_min)
        preference_min = preference_response_min["response"]
        #print("terminando con mp ",preference)
        #print("terminando con mp min ",preference_min)

        cancha_data = {
                'id'       : cancha.id,
                'nombre'   : cancha.nombre,
                'precio'   : cancha.precio,
                'anticipo' : cancha.anticipo,
                'p'        : preference,
                'p_min'    : preference_min
            }
    return JsonResponse(cancha_data, safe=False)


#mp = MercadoPago('206337924', 'APP_USR-49830c2d-5e11-4c81-a9e9-4fd2fc139e92') 

def retorno_pago(request):
    sdk = mercadopago.SDK("APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137")
    mp = sdk.preference().get(request.GET.get('preference_id'))
    #print("MOSTRANDO PAGO ID: ",request.GET.get('payment_id'))
    #print("MOSTRANDO STATUS: ", request.GET.get('status'))
    predio_redirect = Canchas.objects.get(pk=mp['response']['metadata']['cancha_id'])

    #if status==approved
    print("user is auth? ",request.user.is_authenticated)
    if request.user.is_authenticated:
        if request.method == 'GET':
            cancha_id   = mp['response']['metadata']['cancha_id']
            fecha_ini   = mp['response']['metadata']['fecha_ini']
            fecha_fin   = mp['response']['metadata']['fecha_fin']
            precio_cancha   = mp['response']['metadata']['precio_cancha']
            usuario = request.user
            
            reservas = Reservas.objects.filter(cancha_id=cancha_id, fecha_fin__gt=fecha_ini, fecha_ini__lt=fecha_fin).exclude(estado='Cancelado')
            
            if reservas.count() > 0:
                mensaje = f'El horario desde {fecha_ini} hasta {fecha_fin} ,esta ocupado.'

                messages.error(request,mensaje)
            else:

                if request.GET.get('status') == 'approved':
                    try:
                        cancha = Canchas.objects.get(pk=cancha_id)
                    except Canchas.DoesNotExist:
                        # Manejo de error si no se encuentra la cancha
                        # Puedes redirigir o mostrar un mensaje de error aquí
                        messages.error(request, 'Cancha no existente')

                        return redirect('predio',pk=predio_redirect.predio_id.pk)        # Crea una instancia de Reserva con los datos
                    """nueva_reserva = Reservas.objects.create(
                        user_id=usuario,
                        cancha_id=cancha,
                        fecha_ini=fecha_ini,
                        fecha_fin=fecha_fin,
                        precio=mp['response']['items'][0]['unit_price'],
                        anticipo=mp['response']['items'][0]['unit_price']
                    )"""
                    reserva_activa = Reservas.objects.filter(user_id = usuario,cancha_id=cancha).last()
                    reserva_activa.fecha_fin = fecha_fin
                    reserva_activa.precio=mp['response']['items'][0]['unit_price']
                    reserva_activa.anticipo=mp['response']['items'][0]['unit_price']
                    reserva_activa.estado = 'Activo'
                    reserva_activa.save()

                    # Guarda la instancia de Reserva en la base de datos
                    #p = nueva_reserva.save()
                    #reserva_id=Reservas.objects.filter(user_id=usuario,cancha_id=cancha,fecha_fin=fecha_fin,fecha_ini=fecha_ini).last()
                    #grabar_pago(request.GET.get('payment_id'),request.GET.get('status'),mp['response']['items'][0]['unit_price'],nueva_reserva)
                    grabar_pago(request.GET.get('payment_id'),request.GET.get('status'),mp['response']['items'][0]['unit_price'],reserva_activa)
                    
                    datos_send_mail = {
                        'user_name': usuario.first_name,
                        'user_telefono': '4229300',
                        #'mail': usuario.email,
                        'mail': 'josemaria.terrazas@gmail.com',
                        'fecha_ini': fecha_ini,
                        'fecha_fin': fecha_fin,
                        'anticipo':mp['response']['items'][0]['unit_price'],
                        'precio':mp['response']['items'][0]['unit_price'],
                        'predio_nom':cancha.predio_id.nombre,
                        'predio_tele':cancha.predio_id.telefono,
                        'predio_ubicacion':cancha.predio_id.direccion,
                        'predio_email':cancha.predio_id.email,
                        'cancha_nombre':cancha.nombre,
                        'precio_cancha':precio_cancha,
                        #'route':ngrok_url,
                        'route': "https://softwarecancha.onrender.com/",
                    }
                    email.send_cliente_email(datos_send_mail)
                    email.send_predio_email(datos_send_mail,usuario.first_name,cancha.nombre)


                    mensaje = f'Reserva creada desde {fecha_ini} hasta {fecha_fin} con éxito.'

                    # Agregar el mensaje de éxito
                    messages.success(request, mensaje)   
                else:
                    messages.error(request, "No pudimos procesar tu pago.") 
                    reserva_a_eliminar = Reservas.objects.filter(user_id = usuario,cancha_id=Canchas.objects.get(pk=cancha_id)).last()
                    print("ELIMINANDO PRE RESERVA: ",reserva_a_eliminar.pk)
                    reserva_a_eliminar.delete()
                    #return redirect('predio',pk=predio_redirect.predio_id.pk)
                

            #return redirect(previous_url)
            return redirect('predio',pk=predio_redirect.predio_id.pk)
        
    else: 
        mensaje = f'Necesita estar logeado para poder reservar'
        messages.error(request,mensaje)
        #previous_url = request.META.get('HTTP_REFERER', '/')

        #return redirect(previous_url)
        return redirect('predio',pk=predio_redirect.predio_id.pk)


    #return render(request, 'prueba.html',{})

"""from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def notificacion_pago(request):
    print("ENTRO A NOTIFICACION PAGO")
    sdk = mercadopago.SDK("APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137")
    if request.method == "POST":
        #data = request.POST.dict()
        data = request.POST
        print("MOSTRANDO DATA",data)
        #payment = sdk.get_payment(data['id'])
        #print(payment)
        # Procesar la notificación y actualizar el estado de tu pedido
        # Puedes usar el objeto 'payment' para obtener información sobre el pago
        
    return HttpResponse(status=200)"""

def grabar_pago(payment_id,status,monto,reserva_id):
    nuevo_pago = pagos()
    nuevo_pago.payment_id = payment_id
    nuevo_pago.status = status
    nuevo_pago.monto = monto
    nuevo_pago.reserva_id = reserva_id
    nuevo_pago.save()

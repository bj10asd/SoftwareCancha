import datetime
from django import template
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas,usuarios
from datetime import datetime,timedelta
from django.utils import timezone
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_reservas(cancha,hora):
    #print("*********************************** ENTRE A CONSULTA RESERVAS")
    #print("MOSTRANDO HORA",hora)
    hora_fin = hora + timedelta(hours=1)

    #reserva = Reservas.objects.filter(Q(cancha_id=cancha) & (Q(fecha_ini=hora) | Q(fecha_fin=hora_fin))).exclude(estado='Cancelado')
    #print("mostrando cancha id: ",cancha)
    reserva = Reservas.objects.filter(Q(cancha_id=cancha) & (Q(fecha_ini=hora) | Q(fecha_fin=hora_fin))).exclude(estado='Cancelado')
    #print(reserva[0].user_id.first_name or '')
    if reserva.count() > 0:
        return reserva[0].user_id
    else:
        return ""
    
@register.filter(expects_localtime=True)
def is_past(timestamp):
    return timestamp<timezone.now()

@register.simple_tag
def reformat_date(dia):
    d = dia.split("-")
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    d = datetime.strptime(d[2]+"-"+d[1]+"-"+d[0],"%d-%m-%Y")
    print(d)
    return  dias[d.weekday()]+" "+d.strftime("%d-%m-%Y")


@register.simple_tag
def dia_actual(dia_reserva):
    dia_reserva = datetime.strptime(dia_reserva, "%Y-%m-%d")
    today = datetime.now()
    if today.year == dia_reserva.year and today.month == dia_reserva.month and today.day == dia_reserva.day:
        return True
    else:
        return False
    
@register.simple_tag
def get_telefono(user):
    try:#metemos try por si no existe el usuario
        telefono = usuarios.objects.get(user_id = user).telef
    except:
        print("Hubo un error consultando datos del usuario.")
        telefono = 0
    return telefono 


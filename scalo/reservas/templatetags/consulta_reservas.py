import datetime
from django import template
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas
from datetime import datetime,timedelta
from django.utils import timezone
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_reservas(cancha,hora):
    hora_fin = hora + timedelta(hours=1)

    reserva = Reservas.objects.filter(Q(cancha_id=cancha) & (Q(fecha_ini=hora) | Q(fecha_fin=hora_fin)))

    if reserva.count() > 0:
        return(reserva[0].user_id)
    else:
        return ""
    
@register.filter(expects_localtime=True)
def is_past(timestamp):
    return timestamp<timezone.now()

@register.simple_tag
def reformat_date(dia):
    d = dia.split("-")
    return d[2]+"-"+d[1]+"-"+d[0]
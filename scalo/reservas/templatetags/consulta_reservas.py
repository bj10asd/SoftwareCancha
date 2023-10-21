import datetime
from django import template
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_reservas(cancha,hora):
    reserva = Reservas.objects.filter(cancha_id=cancha,fecha_ini=hora)
    if reserva.count() > 0:
        print(reserva[0].user_id)
        return(reserva[0].user_id)
    else:
        print("No devuelve nada")
        return ""
    
@register.filter(expects_localtime=True)
def is_past(timestamp):
    return timestamp<timezone.now()
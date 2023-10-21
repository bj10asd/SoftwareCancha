import datetime
from django import template
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas
from datetime import datetime ,timedelta
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_reservas(cancha,hora):
    hora_fin = hora + timedelta(hours=1)

    reserva = Reservas.objects.filter(Q(cancha_id=cancha) & (Q(fecha_ini=hora) | Q(fecha_fin=hora_fin)))

    if reserva.count() > 0:
        print(reserva[0].user_id) 
        return(reserva[0].user_id)
    else:
        print("No devuelve nada")
        return ""
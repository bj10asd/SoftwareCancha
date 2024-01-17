import datetime
from django import template
from reservas.models import UsuarioXRoles,Roles,Predios,Deportes,Canchas,Reservas,usuarios
from datetime import datetime,timedelta
from django.utils import timezone
from django.db.models import Q
import requests
import json

register = template.Library()

@register.simple_tag
def get_perfil_predio(klave):
    url = "https://5jt.000webhostapp.com/get_photos.php"

    # Datos que deseas enviar en la solicitud POST
    data_to_send = {
        #'klave': 'estelaevelia.herrera@gmail.com'
        'klave': klave+"_p"
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
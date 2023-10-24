
# Registar una reserva
> Como usuario registrado  
necesito registrar una reserva de una cancha
para asegurarme de tener un espacio y horario disponible para disfrutar de la actividad planificada

## Criterios de Validación
- En la lista de canchas de un predio se debe poder ver los horarios en las que:
    - La cancha esta ocupada (Color gris oscuro)
    - La cancha está disponible (Color blanco)
    - Reservas del usuario (Color celeste)
- Mostrar la fecha de la cual se muestran los horarios de las canchas
- La fecha debe tener el siguiente formato: *DD/MM/AAAA*
- Se debe poder navegar entre los días.
- Al seleccionar un horario para reservar se debe desplegar una ventana modal que muestre:
    - Nombre del predio
    - Nombre de la cancha en la cual se esta reservando
    - Hora seleccionada
    - Un combo box que permita seleccionar la duracion (60 min o 120 min)
    - Precio de la reserva
    - Boton para confirmar la reserva
- Al confirmar la reserva mostrar una alerta de "Reserva realizada exitosamente"
- En caso de querer reservar en un horario no disponible, mostrar un popover con el mensaje "Cancha no disponible para este horario".
- Si quiero reservar no estando logueado, debo mostrar un popover con la posiblidad de redirigir a iniciar sesion.
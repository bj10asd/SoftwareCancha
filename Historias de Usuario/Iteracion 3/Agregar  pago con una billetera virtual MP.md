# Agregar pago con una billetera vritual MP
> Como Cliente
necesito integrar mercado pago
para facilitar el pago de mis reserva.

## Criterios de Validación
-Sobre el modal de confirmar reserva
-Se aceptan pagos con Saldo de MP, Tarjeta de Debito y Tarjeta de Credito.
-Si la reserva es de 120 minutos el preciodel  anticipo es el doble.
-El pago se debe acreditar a la cuenta de Mercado Pago del propietario.
-Agregar en la parte inferior un button con el texto "Confirmar " + icon de MP,
rediriguiendo a la pagina de mercado pago , mostrando como titulo el nombre de la cancha y del predio, con el precio del anticipo de la cancha y una descripcion 
"Pago de Anticipo de reserva en Reserva Total".
-Si el pago es aceptado, se registra la reserva y se muestra con alert con el mensaje "Reserva creada desde 2023-10-26 15:00 hasta 2023-10-26 16:00 con éxito.".
-Si el pago denegado por algun motivo,se muestra un alert con el mensaje 
"Reserva denegada por, {{Motivo}} sobre el pago"

from modelos.usuario import Usuario
from modelos.tipoEntrada import TipoEntrada
from modelos.formaPago import FormaPago
from modelos.detalleEntrada import DetalleEntrada
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Entrada:

    def __init__(self , usuario, cantidad,fecha_visita, forma_pago, detalles_entrada, fecha_compra=date.today()):

        self.usuario = usuario
        self.cantidad = cantidad
        self.fecha_visita = fecha_visita
        self.forma_pago = forma_pago
        self.detalles_entrada = detalles_entrada
        self.fecha_compra = fecha_compra
        self.estado_pago = "pendiente"

    
    def monto_total(self):

        total = 0

        for detalle in self.detalles_entrada:
            total += detalle.calcular_monto()
        return total
    

    def validarCantidadEntradas(self):

        if self.cantidad <1 or self.cantidad >10:
            raise ValueError("La cantidad de entradas no es válida.")
        else:
            return True
    

    def validarFechaVisita(self):

        if self.fecha_visita is None:
            raise ValueError("La fecha de visita no puede ser nula.")
        
        elif self.fecha_visita < self.fecha_compra:
            raise ValueError("La fecha de visita no puede ser anterior a la fecha de compra.")

        elif self.fecha_visita.weekday() == 0:
            raise ValueError("La fecha de visita no puede ser un lunes (día de cierre).")
        
        elif self.fecha_visita in [date(self.fecha_visita.year, 1, 1),
                                  date(self.fecha_visita.year, 12, 25)]:
            raise ValueError("La fecha de visita es un día festivo.")
        
        else:
            return True
    

    def procesar_pago(self):

        monto = self.monto_total()
        pago =self.forma_pago.procesar_pago(monto) #pago es un diccionario que contiene "status": "approved", "id_pago": 12345}   # si fue aprobado{"status": "rejected", "error": "Fondos insuficientes"}   # si fue rechazado
        self.estado_pago = pago["status"]

        if pago["status"] == "approved":
            self.monto_total_pagado = self.monto_total()

            asunto = "Confirmación de compra en EcoHarmony"
            cuerpo = (
                f"Hola {self.usuario.mail},\n\n"
                f"Tu compra fue confirmada exitosamente.\n"
                f"Cantidad de entradas: {self.cantidad}\n"
                f"Monto pagado: ${monto}\n"
                f"Fecha de visita: {self.fecha_visita}\n\n"
                "¡Gracias por tu compra y que disfrutes tu visita!"
            )

            try:
                # Intentar enviar el mail real
                self.enviar_mail(self.usuario.mail, asunto, cuerpo)
                print(f"Mail de confirmación enviado a {self.usuario.mail}")
            except Exception as e:
                # Si hay error, lo mostramos (pero no interrumpimos la compra)
                print(f"⚠️ Error al enviar mail: {e}")
        
        return pago
    

    def enviar_mail(self, destinatario, asunto, cuerpo):
        
        if destinatario and asunto and cuerpo:
            estado = "approved" # Simulamos que el mail fue enviado
            return {
                "status": estado,
                "mensaje": f"Mail enviado a {destinatario} con asunto '{asunto}'",
                "cuerpo": cuerpo
            }
        else:
            raise ValueError("Faltan datos para enviar el mail.")

    
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base_de_datos

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
    

    def validar_cantidad_entradas(self):

        if self.cantidad <1 or self.cantidad >10:
            raise ValueError("La cantidad de entradas no es válida.")
        else:
            return True
    

    def validar_fecha_visita(self):

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


    # --- Nuevo método auxiliar para generar el HTML del correo ---
    def _generar_html_compra(self):
        # Datos para el HTML
        fecha_visita_str = self.fecha_visita.strftime("%d/%m/%Y")
        
        # Generar la lista de participantes para el HTML
        participantes_html = ""
        for detalle in self.detalles_entrada:
            # Asumo que detalle tiene edad_visitante y tipo_entrada (con nombre)
            tipo_entrada_nombre = getattr(detalle.tipo_entrada, 'nombre', str(detalle.tipo_entrada)).capitalize()
            # NOTA: No tengo DNI ni Nombre completo del visitante aquí, uso edad y tipo.
            participantes_html += (
                f'<li style="margin-bottom: 5px;">'
                f'Tipo: {tipo_entrada_nombre}, Edad: {detalle.edad_visitante}, Precio: ${detalle.calcular_monto()}'
                f'</li>'
            )
        
        # Uso los colores oficiales
        ECO_DARK = "#134611"
        ECO_MEDIUM = "#3E8914"
        ECO_BRIGHT = "#3DA35D"
        ECO_LIGHT = "#96E072"
        ECO_BG = "#E8FCCF"
        
        # HTML del cuerpo del correo (simplificado y adaptado al contexto de Compra)
        html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Confirmación de Compra - EcoHarmony Park</title>
            </head>
            <body style="margin: 0; padding: 0; background-color: {ECO_BG}; font-family: Monserrat, sans-serif; color: {ECO_DARK};">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: {ECO_BG};">
                    <tr>
                        <td align="center" style="padding: 20px 0;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                                <tr>
                                    <td style="padding: 0;">
                                        
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: {ECO_DARK}; color: white; border-radius: 8px 8px 0 0;">
                                            <tr>
                                                <td align="center" style="padding: 20px;">
                                                    <img src="https://drive.google.com/uc?export=view&id=1ezfHz4VPbjdRINLmbSF_zRv8vT5wsVaa" alt="Logo EcoHarmony" width="60" style="display: block; margin: 0 auto 10px; filter: invert(1);">
                                                    <h2 style="margin: 0; font-size: 24px;">EcoHarmony Park</h2>
                                                </td>
                                            </tr>
                                        </table>

                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="padding: 20px 40px; color: {ECO_DARK};">
                                            <tr>
                                                <td style="text-align: center; padding-bottom: 20px;">
                                                    <p style="font-size: 20px; font-weight: bold; color: {ECO_MEDIUM}; margin: 0;">
                                                        &#x2705; ¡Compra Confirmada!
                                                    </p>
                                                    <p style="font-size: 14px; line-height: 1.5; margin-top: 15px;">
                                                        Tu compra fue registrada correctamente. A continuación, encontrarás los detalles de tu reserva para la visita.
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>

                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="90%" align="center" style="margin-bottom: 25px; border-radius: 5px; overflow: hidden; border: 1px solid {ECO_BRIGHT};">
                                            <tr>
                                                <td style="padding: 10px 20px; font-weight: bold; background-color: {ECO_LIGHT};">Fecha de Visita:</td>
                                                <td style="padding: 10px 20px; background-color: {ECO_BG};">{fecha_visita_str}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px 20px; font-weight: bold; background-color: {ECO_LIGHT};">Total Entradas:</td>
                                                <td style="padding: 10px 20px; background-color: {ECO_BG};">{self.cantidad}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px 20px; font-weight: bold; background-color: {ECO_LIGHT};">Monto Pagado:</td>
                                                <td style="padding: 10px 20px; background-color: {ECO_BG};">${self.monto_total()}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 10px 20px; font-weight: bold; background-color: {ECO_LIGHT};">Correo de contacto:</td>
                                                <td style="padding: 10px 20px; background-color: {ECO_BG};">
                                                    <a href="mailto:{self.usuario.mail}" style="color: {ECO_MEDIUM}; text-decoration: none;">{self.usuario.mail}</a>
                                                </td>
                                            </tr>
                                        </table>

                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="90%" align="center" style="margin-bottom: 25px;">
                                            <tr>
                                                <td style="font-weight: bold; color: {ECO_MEDIUM}; padding: 0 0 10px 0;">&#x25CF; Detalle de Entradas:</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 15px 20px; background-color: {ECO_BG}; border-radius: 5px; border: 1px solid {ECO_LIGHT};">
                                                    <ul style="list-style-type: disc; margin: 0; padding-left: 20px; font-size: 14px;">
                                                        {participantes_html}
                                                    </ul>
                                                </td>
                                            </tr>
                                        </table>

                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="90%" align="center" style="margin-bottom: 25px;">
                                            <tr>
                                                <td style="text-align: center; color: {ECO_DARK}; font-size: 16px; font-weight: bold;">
                                                    ¡Gracias por tu compra y que disfrutes tu visita el {fecha_visita_str}!
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: {ECO_MEDIUM}; color: white; border-radius: 0 0 8px 8px;">
                                            <tr>
                                                <td align="center" style="padding: 10px; font-size: 12px;">
                                                    Este es un mensaje automático, por favor no respondas a este correo.
                                                </td>
                                            </tr>
                                        </table>
                                        
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
            </html>
            """
        return html_body


    def procesar_pago(self, enviar_mail=True):
        """
        Procesa el pago (simulación) y devuelve el estado.
        Ya no guarda en la base de datos directamente.
        """

        monto = self.monto_total()
        pago = self.forma_pago.procesar_pago(monto)
        self.estado_pago = pago["status"]

        #  Si el pago fue aprobado, guardamos el monto pagado. Si no, 0.
        self.monto_total_pagado = monto if pago["status"] == "approved" else 0

        # Si el pago fue aprobado, enviar mail de confirmación (usar datos internos)
        if pago["status"] == "approved" and enviar_mail:
            try:
                asunto = "Confirmación de compra EcoHarmony"
                cuerpo_texto = f"Tu compra fue aprobada. Monto: ${monto}"
                cuerpo_html = self._generar_html_compra()
                # destinatario tomado desde el usuario asociado
                destinatario = getattr(self.usuario, 'mail', None)
                if destinatario:
                    # Usar el método enviar_mail; durante tests se parchea para evitar envíos reales
                    self.enviar_mail(destinatario, asunto, cuerpo_texto, cuerpo_html)
            except Exception:
                # No hacer fallar el procesamiento por errores de envío de email (sólo loguear)
                pass

        # Solo devuelve el resultado, sin guardar
        return pago


    def enviar_mail(self, destinatario, asunto, cuerpo_texto, cuerpo_html=None): # Modificación en la firma
        
        remitente = "ecoharmonyparque@gmail.com"
        contraseña = "nujk erab chhu bous" # Contraseña de aplicación

        #  Crear el mensaje como MIMEMultipart
        mensaje = MIMEMultipart("alternative") # "alternative" es clave para texto/html
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = asunto

        #  Adjuntar el cuerpo de texto plano
        mensaje.attach(MIMEText(cuerpo_texto, "plain"))

        #  Adjuntar el cuerpo HTML (si existe)
        if cuerpo_html:
            mensaje.attach(MIMEText(cuerpo_html, "html")) # Cambiamos 'plain' por 'html'

        #  Conectar con el servidor SMTP de Gmail
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
                servidor.starttls()
                servidor.login(remitente, contraseña)
                servidor.send_message(mensaje)

            print(f"✅ Mail enviado correctamente a {destinatario}")
        except Exception as e:
            print(f"❌ Error al enviar mail: {e}")
            raise e
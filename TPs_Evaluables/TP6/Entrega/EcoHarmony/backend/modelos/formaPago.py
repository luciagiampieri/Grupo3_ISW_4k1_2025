class FormaPago:

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
    

    def procesar_pago(self, monto):
        # Si el pago es con tarjeta, simulamos que va a Mercado Pago
        print( f"Procesando pago de ${monto} con {self.nombre}..." )
        if "tarjeta" in self.nombre.lower():
            estado = "approved" # Simulamos que el pago fue aprobado
            return {
                "status": estado,
                "mensaje": f"Pago con tarjeta: {estado}",
                "redirect_url": "https://www.mercadopago.com/pago_simulado"
            }
        else:
            # Pago en efectivo (no necesita redirección)
            return {"status": "approved", "mensaje": "Pago en boletería"}
    

    

    

    
# quiero importar la funcion enviar_mail desde backend/modelos/entrada.py y usarla para enviar un mail de prueba
from modelos.entrada import Entrada
from modelos.detalleEntrada import DetalleEntrada


def main():
    detalle = DetalleEntrada(20, "VIP")
    entrada = Entrada(1,"jpenafort13@gmail.com", 2025-10-26, "Efectivo", [detalle], 2025-10-20)
    destinatario = "jpenafort13@gmail.com"
    asunto = "Prueba de envío de mail"
    cuerpo = "Hola Tici! Este es un mail de prueba enviado desde Python 🐍"

    entrada.enviar_mail(destinatario, asunto, cuerpo)

if __name__ == "__main__":
    main()
import pytest
from datetime import date
from backend.models.Entrada import Entrada
from backend.models.DetalleEntrada import DetalleEntrada
from backend.models.FormaPago import FormaPago
from backend.models.TipoEntrada import TipoEntrada
from backend.models.Usuario import Usuario


class TestCompra:

      # Tests que Faltan:
      # - Que haya una BD y que esté cargada.
      # - Los de creación de los objetos.
      # - Los de asociaciones/herencia/composición entre objetos.

      @pytest.fixture
      def entrada(self):
            # --- Precondiciones ---
            tipo = TipoEntrada(id_tipo_entrada=1, nombre="regular", descripcion="Entrada general", precio=5000)
            usuario = Usuario(id_usuario=1, contraseña="1234", mail="fachi@gmail.com")
            forma_pago = FormaPago(id_forma_pago=1, nombre="tarjeta débito", descripcion="Pago con tarjeta")
            detalles = [
                  DetalleEntrada(id_detalle_entrada=1, edad_visitante=30, monto=5000),
                  DetalleEntrada(id_detalle_entrada=2, edad_visitante=9, monto=2500)
            ]

            # --- Pasos del caso de prueba ---
            entrada = Entrada(
                  id_entrada=1,
                  tipo_entrada=tipo,
                  fecha_compra=date(2025, 10, 20),
                  cantidad=len(detalles),
                  usuario=usuario,
                  fecha_visita=date(2025, 10, 23),
                  forma_pago=forma_pago,
                  detalles=detalles
            )

            # --- Resultados esperados ---
            return entrada


      def test_validar_cantidad(self):

            # --- Precondiciones ---
            detalles1 = [DetalleEntrada(edad_visitante=25) for _ in range(10)]
            detalles2 = [DetalleEntrada(edad_visitante=25) for _ in range(3)]

            entrada1 = Entrada(cantidad=10, detalles=detalles1)
            entrada2 = Entrada(cantidad=3, detalles=detalles2)

            # --- Pasos del caso de prueba ---
            e1 = entrada1.validarCantidadEntradas()
            e2 = entrada2.validarCantidadEntradas()

            # --- Resultados esperados ---
            assert e1 == True
            assert e2 == True

            print("✅ Test validar cantidad pasó correctamente.")
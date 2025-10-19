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
      

      def test_validar_cantidad_invalida(self):

            # --- Precondiciones ---
            detalles = [DetalleEntrada(edad_visitante=20)] # Crea un detalle de entrada con edad 20 
            entradas = [
                  Entrada(cantidad=0, detalles=[]), # Cantidad 0, detalles vacíos
                  Entrada(cantidad=-2, detalles=[]), # Cantidad negativa, detalles vacíos
                  Entrada(cantidad=11, detalles=detalles * 11) 
            ]

            # --- Pasos del caso de prueba ---
            resultados = [e.validarCantidadEntradas() for e in entradas] 

            # --- Resultados esperados ---
            assert all(r == False for r in resultados)

            print("✅ Test validar cantidad inválida pasó correctamente.")


      def test_fecha_valida(self):

            # --- Precondiciones ---
            entrada_hoy = Entrada(fecha_visita=date.today())
            entrada_futuro = Entrada(fecha_visita=date(2025, 11, 15))

            # --- Pasos del caso de prueba ---
            r1 = entrada_hoy.validarFecha()
            r2 = entrada_futuro.validarFecha()

            # --- Resultados esperados ---
            assert r1 == True
            assert r2 == True

            print("✅ Test fecha válida pasó correctamente.")

      
      def test_fecha_invalida(self):

            # --- Precondiciones ---
            fechas = [date(2025, 9, 23), date(2025, 1, 1), date(2025, 12, 25), date(2025, 10, 27)]

            # --- Pasos del caso de prueba ---
            resultados = [Entrada(fecha_visita=f).validarFecha() for f in fechas]

            # --- Resultados esperados ---
            assert all(r == False for r in resultados)

            print("✅ Test fecha inválida pasó correctamente.")


      def test_usuario_registrado(self):

            # --- Precondiciones ---
            usuario = Usuario(mail="lucia@gmail.com")

            # --- Pasos del caso de prueba ---
            resultado = usuario.esUsuarioRegistrado()

            # --- Resultados esperados ---
            assert resultado == True

            print("✅ Test usuario registrado pasó correctamente.")

      def test_usuario_no_registrado(self):

            # --- Precondiciones ---
            usuario = Usuario(mail="lucia")

            # --- Pasos del caso de prueba ---
            resultado = usuario.esUsuarioRegistrado()

            # --- Resultados esperados ---
            assert resultado == False

            print("✅ Test usuario no registrado pasó correctamente.")

      
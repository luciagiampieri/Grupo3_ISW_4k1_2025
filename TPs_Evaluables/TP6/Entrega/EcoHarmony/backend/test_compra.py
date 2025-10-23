from unittest.mock import Mock, patch
import pytest
from modelos.tipoEntrada import TipoEntrada
from modelos.usuario import Usuario
from modelos.formaPago import FormaPago
from modelos.entrada import Entrada
from modelos.detalleEntrada import DetalleEntrada
from datetime import date
from unittest.mock import Mock, patch
import pytest
from modelos.tipoEntrada import TipoEntrada
from modelos.usuario import Usuario
from modelos.formaPago import FormaPago
from modelos.entrada import Entrada
from modelos.detalleEntrada import DetalleEntrada
from datetime import date


class TestCompra:

    @pytest.fixture #son los datos que se van a usar en todos los tests, el resto de datos se crean en cada test porque varian segun lo que se quiera probar
    def datosTests(self):
        # --- Precondiciones ---
        tipo1 = TipoEntrada(nombre="regular", descripcion="Entrada general", precio=5000)
        tipo2 = TipoEntrada(nombre="VIP", descripcion="Entrada VIP", precio=10000)
        usuario = Usuario(mail="fachi@gmail.com")
        forma_pago = FormaPago(nombre="tarjeta débito", descripcion="Pago con tarjeta")

        return tipo1,tipo2, usuario, forma_pago


    def test_validar_cantidad_valida(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # Límite mínimo
        detalles1 = [DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1) for _ in range(1)]
        entrada1 = Entrada(usuario=usuario, cantidad=1, fecha_visita=date(2025,10,23),
                           forma_pago=forma_pago, detalles_entrada=detalles1)
        assert entrada1.validar_cantidad_entradas() == True

        # Límite máximo
        detalles10 = [DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1) for _ in range(10)]
        entrada10 = Entrada(usuario=usuario, cantidad=10, fecha_visita=date(2025,10,23),
                            forma_pago=forma_pago, detalles_entrada=detalles10)
        assert entrada10.validar_cantidad_entradas() == True
    

    def test_validar_cantidad_invalida(self, datosTests):

        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # Menor que el límite mínimo
        detalles0 = []
        entrada0 = Entrada(usuario=usuario, cantidad=0, fecha_visita=date(2025,10,23),
                           forma_pago=forma_pago, detalles_entrada=detalles0)
        with pytest.raises(ValueError):
            entrada0.validar_cantidad_entradas()

        # Mayor que el límite máximo
        detalles11 = [DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1) for _ in range(11)]
        entrada11 = Entrada(usuario=usuario, cantidad=11, fecha_visita=date(2025,10,23),
                            forma_pago=forma_pago, detalles_entrada=detalles11)
        with pytest.raises(ValueError):
            entrada11.validar_cantidad_entradas()
    

    def test_validar_fecha_visita_valida(self, datosTests):
        
        # precondiciones
        tipo1, tipo2, usuario, forma_pago = datosTests

        detalles = [DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1) for _ in range(5)]
        entrada = Entrada(usuario=usuario, cantidad=5, fecha_visita=date(2025,10,25),
                                 forma_pago=forma_pago, detalles_entrada=detalles) #creacion de la entrada con fecha valida
        
        # pasos para probar
        resultado = entrada.validar_fecha_visita()

        #resultado esperado
        assert resultado == True
    

    def test_validar_fecha_visita_invalida(self, datosTests):

        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        casos_invalidos = [
            date(2024, 12, 31),  # fecha anterior a la compra
            date(2025, 10, 20),  # lunes
            date(2025, 1, 1),    # feriado 1 enero
            date(2025, 12, 25)   # feriado 25 diciembre
        ]

        # Pasos para probar cada caso inválido
        for fecha in casos_invalidos:
            detalles = [DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1) for _ in range(5)]
            entrada = Entrada(
                usuario=usuario,
                cantidad=5,
                fecha_visita=fecha,
                forma_pago=forma_pago,
                detalles_entrada=detalles
            )

            # Resultado esperado es que se lance ValueError para cada caso inválido
            with pytest.raises(ValueError):
                entrada.validar_fecha_visita()
            

    def test_usuario_registrado(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # pasos para probar
        resultado = usuario.validar_usuario_registrado("fachi@gmail.com")

        #resultado esperado
        assert resultado == True


    def test_usuario_no_registrado(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # pasos para probar
        resultado = usuario.validar_usuario_registrado("noexiste@gmail.com")

        #resultado esperado
        assert resultado == False
    

    def test_monto_total(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        detalles = [
            DetalleEntrada(edad_visitante=5, tipo_entrada=tipo1),   # 50% descuento
            DetalleEntrada(edad_visitante=30, tipo_entrada=tipo2),  # precio completo
            DetalleEntrada(edad_visitante=70, tipo_entrada=tipo1)   # 50% descuento
        ]
        entrada = Entrada(usuario=usuario, cantidad=3, fecha_visita=date(2025,10,23),
                               forma_pago=forma_pago, detalles_entrada=detalles)

        # pasos para probar
        # monto_esperado = (tipo1.precio * 0.5) + tipo2.precio + (tipo1.precio * 0.5)
        monto_esperado = 15000

        #resultado esperado
        assert entrada.monto_total() == monto_esperado


    def test_monto_total_invalido(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        detalles = [
            DetalleEntrada(edad_visitante=5, tipo_entrada=tipo1),   # 50% descuento
            DetalleEntrada(edad_visitante=30, tipo_entrada=tipo2),  # precio completo
            DetalleEntrada(edad_visitante=70, tipo_entrada=tipo1)   # 50% descuento
        ]
        entrada = Entrada(usuario=usuario, cantidad=3, fecha_visita=date(2025,10,23),
                               forma_pago=forma_pago, detalles_entrada=detalles)
        
        # pasos para probar
        monto_incorrecto = 20000  # Valor incorrecto intencionalmente

        #resultado esperado
        assert entrada.monto_total() != monto_incorrecto
    

    def test_pago_aprobado_mp(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # Creamos un mock que reemplaza el método procesar_pago de la forma de pago
        forma_pago_mock = Mock()
        forma_pago_mock.procesar_pago.return_value = {"status": "approved", "id_pago": 12345, "redirect_url": "https://www.mercadopago.com/pago_simulado"}

        entrada = Entrada(
            usuario=usuario,
            cantidad=1,
            fecha_visita=date(2025,10,23),
            forma_pago=forma_pago_mock,
            detalles_entrada=[DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1)]
        )

        # El patch nos permite reemplazar el método enviar_mail temporalmente por una función mock, para que no se envíe un mail real durante la prueba
        with patch.object(Entrada, "enviar_mail") as mock_mail:
            resultado = entrada.procesar_pago()
        
            #resultado esperado
            assert resultado["status"] == "approved"
            assert "redirect_url" in resultado # En caso de rechazo, también hay URL de redirección
    

    def test_pago_rechazado_mp(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # Creamos un mock que reemplaza el método procesar_pago
        forma_pago_mock = Mock()
        forma_pago_mock.procesar_pago.return_value = {"status": "rejected", "error": "Fondos insuficientes", "redirect_url": "https://www.mercadopago.com/pago_simulado"}

        entrada = Entrada(
            usuario=usuario,
            cantidad=1,
            fecha_visita=date(2025,10,23),
            forma_pago=forma_pago_mock,
            detalles_entrada=[DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1)]
        )

         # El patch nos permite reemplazar el método enviar_mail temporalmente por una función mock, para que no se envíe un mail real durante la prueba
        with patch.object(Entrada, "enviar_mail") as mock_mail:
            resultado = entrada.procesar_pago()
        
            #resultado esperado
            assert resultado["status"] == "rejected"
            assert "redirect_url" in resultado # En caso de rechazo, también hay URL de redirección
    

    def test_pago_efectivo(self, datosTests):
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests
        forma_pago = FormaPago(nombre="efectivo", descripcion="Pago en boletería")

        entrada = Entrada(
            usuario=usuario,
            cantidad=1,
            fecha_visita=date(2025,10,23),
            forma_pago=forma_pago,
            detalles_entrada=[DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1)]
        )

        # El patch nos permite reemplazar el método enviar_mail temporalmente por una función mock, para que no se envíe un mail real durante la prueba
        with patch.object(Entrada, "enviar_mail") as mock_mail:
            resultado = entrada.procesar_pago()
        
            #resultado esperado
            assert resultado["status"] == "approved"
            assert "redirect_url" not in resultado # En caso de rechazo, también hay URL de redirección
    

    def test_envio_mail_pago_aprobado(mock_enviar_mail, datosTests):

        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        forma_pago_mock = Mock()
        forma_pago_mock.procesar_pago.return_value = {"status": "approved", "id_pago": 1}


        entrada = Entrada(
            usuario=usuario,
            cantidad=1,
            fecha_visita=date(2025, 10, 23),
            forma_pago=forma_pago_mock,
            detalles_entrada=[DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1)]
        )

        with patch.object(entrada, "enviar_mail") as mock_mail:
            resultado = entrada.procesar_pago()
            assert resultado["status"] == "approved"
            mock_mail.assert_called_once()  # Verifica que se llamó a enviar_mail
    

    def test_atributos_entrada(self, datosTests): # verifica que los atributos de la clase Entrada se crean correctamente
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        detalles = [
            DetalleEntrada(edad_visitante=5, tipo_entrada=tipo1),   # 50% descuento
            DetalleEntrada(edad_visitante=30, tipo_entrada=tipo2),  # precio completo
        ]
        entrada = Entrada(usuario=usuario, cantidad=2, fecha_visita=date(2025,10,23),
                               forma_pago=forma_pago, detalles_entrada=detalles)

        # Verificar que los atributos existen
        assert hasattr(entrada, 'fecha_compra')
        assert hasattr(entrada, 'cantidad')
        assert hasattr(entrada, 'usuario')
        assert hasattr(entrada, 'fecha_visita')
        assert hasattr(entrada, 'forma_pago')
        assert hasattr(entrada, 'detalles_entrada')
        assert hasattr(entrada, 'estado_pago')

        # verificar que el atributo usuario es una instancia de Usuario
        assert isinstance(entrada.usuario, Usuario)
        assert isinstance(entrada.forma_pago, FormaPago)
        assert all(isinstance(detalle, DetalleEntrada) for detalle in entrada.detalles_entrada)
    

    def test_atributos_detalle_entrada(self, datosTests): # verifica que los atributos de la clase DetalleEntrada se crean correctamente
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        detalle = DetalleEntrada(edad_visitante=25, tipo_entrada=tipo1)

        # Verificar que los atributos existen
        assert hasattr(detalle, 'edad_visitante')
        assert hasattr(detalle, 'tipo_entrada') 

        # verificar que el atributo tipo es una instancia de TipoEntrada
        assert isinstance(detalle.tipo_entrada, TipoEntrada)
    

    def test_atributos_forma_pago(self, datosTests): # verifica que los atributos de la clase FormaPago se crean correctamente
        # --- Precondiciones ---
        tipo1, tipo2, usuario, forma_pago = datosTests

        # Verificar que los atributos existen
        assert hasattr(forma_pago, 'nombre')
        assert hasattr(forma_pago, 'descripcion')



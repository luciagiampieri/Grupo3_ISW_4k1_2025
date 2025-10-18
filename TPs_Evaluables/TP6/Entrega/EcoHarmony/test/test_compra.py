from backend.utils import (
      validarCantidadEntradas
)

class TestCompra:

      # 1. Validar cantidad de entradas
      def test_validar_cantidad(self):
            # --- Precondiciones ---
            cantidad1 = 10 # Cantidad válida de entradas que el usuario puede comprar, la cantidad maxima es 10
            cantidad2 = 3  # Cantidad mínima válida de entradas que el usuario puede comprar

            # --- Pasos del caso de prueba ---
            resultado1 = validarCantidadEntradas(cantidad1) #la funcion validar entrada, va a devolver True o False de acuerdo a la cantidad seleccionada
            resultado2 = validarCantidadEntradas(cantidad2)

            # --- Resultados esperados ---
            assert resultado1 == True
            assert resultado2 == True


            # --- Mensaje final ---
            print("✅ Test validar cantidad pasó correctamente.")


def test_validar_cantidad_invalida(self): #en esta poner todos los casos invalidos, porque estamos probando lo mismo 
            # --- Precondiciones ---
            cantidad1 = 0 # cantidad inv
            cantidad2 = -2 # cantidad invalida negativa
            cantidad3 = 11 # cantidad invalida mayor a 10

            # --- Pasos del caso de prueba ---
            resultado1 = validarCantidadEntradas(cantidad1)
            resultado2 = validarCantidadEntradas(cantidad2)
            resultado3 = validarCantidadEntradas(cantidad3)

            # --- Resultados esperados ---
            assert resultado1 == False
            assert resultado2 == False
            assert resultado3 == False

            # --- Mensaje final ---
            print("✅ Test validar cantidad inválida pasó correctamente.")
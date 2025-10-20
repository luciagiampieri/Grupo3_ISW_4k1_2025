from modelos.tipoEntrada import TipoEntrada

class DetalleEntrada:

    def __init__(self, edad_visitante, tipo_entrada):
        self.monto = 0
        self.edad_visitante = edad_visitante
        self.tipo_entrada = tipo_entrada
    
    def validar_edad(self):
        if self.edad_visitante <0 or self.edad_visitante >120:
            raise ValueError("La edad del visitante no es válida.")
        else:
            return True
        
    def calcular_monto(self):
        
        if self.edad_visitante <10 or self.edad_visitante > 60:
            self.monto = self.tipo_entrada.precio * 0.5
        else:
            self.monto = self.tipo_entrada.precio
        return self.monto
    
    

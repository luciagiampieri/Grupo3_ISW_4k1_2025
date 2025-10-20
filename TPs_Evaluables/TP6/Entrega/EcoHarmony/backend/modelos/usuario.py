class Usuario:

    usuarios_registrados = ["fachi@gmail.com", "tici@gmail.com", "juan@mail.com"]

    def __init__(self, mail):
        self.mail = mail
        

    def validar_usuario_registrado(self, mail):

        for usuario in self.usuarios_registrados:
            if usuario == mail:
                return True
        return False
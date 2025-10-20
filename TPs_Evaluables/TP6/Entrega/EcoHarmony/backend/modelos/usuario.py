import base_de_datos


class Usuario:

    def __init__(self, mail):
        self.mail = mail

    def validar_usuario_registrado(self, mail: str) -> bool:
        """Verifica en la base de datos si el usuario está registrado.

        Retorna True si existe, False en caso contrario.
        """
        conn = base_de_datos.get_connection()
        try:
            cur = conn.cursor()
            cur.execute('SELECT id FROM usuario WHERE email = ?', (mail,))
            row = cur.fetchone()
            return row is not None
        finally:
            conn.close()
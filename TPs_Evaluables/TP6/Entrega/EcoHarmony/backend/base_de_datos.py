import sqlite3
import os
from typing import Optional, Tuple

# Guardar la base de datos en el mismo directorio de este archivo (backend/ecoharmony.db)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ecoharmony.db')


def get_connection():
    """Returna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    # usar row_factory para acceder por nombre de columna si hace falta
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas necesarias si no existen y deja algunos datos de prueba.

    Llama a esta función al inicio de la aplicación o antes de ejecutar tests.
    """
    # Comprobar si ya existe el archivo de la base de datos para evitar crear
    # una copia en otro directorio cuando se ejecuta el script desde otro CWD.
    db_exists = os.path.exists(DB_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    # tabla usuario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL
    );
    ''')

    # tabla tipoEntrada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipoEntrada (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL
    );
    ''')

    # tabla formaPago
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS formaPago (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT
    );
    ''')

    # tabla entrada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entrada (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha_visita TEXT NOT NULL,
        forma_pago_id INTEGER NOT NULL,
        fecha_compra TEXT NOT NULL,
        estado_pago TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id),
        FOREIGN KEY (forma_pago_id) REFERENCES formaPago(id)
    );
    ''')

    # tabla detalleEntrada
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalleEntrada (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        edad_visitante INTEGER NOT NULL,
        tipo_entrada_id INTEGER NOT NULL,
        entrada_id INTEGER NOT NULL,
        FOREIGN KEY (tipo_entrada_id) REFERENCES tipoEntrada(id),
        FOREIGN KEY (entrada_id) REFERENCES entrada(id)
    );
    ''')

    # Insertar algunos usuarios de prueba si no existen. Siempre intentamos
    # insertar con OR IGNORE; esto es seguro tanto si la DB se creó ahora como
    # si ya existía pero faltaban registros.
    try:
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("fachi@gmail.com",))
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("tici@gmail.com",))
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("juan@mail.com",)),
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("jpenafort13@gmail.com",)),
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("mickaelacrespo@gmail.com",)),
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("francogiorda@gmail.com",))
        cursor.execute('INSERT OR IGNORE INTO usuario (email) VALUES (?)', ("manuviale123@gmail.com",))
        cursor.execute('INSERT INTO tipoEntrada (nombre, descripcion, precio) VALUES (?, ?, ?)', ("regular", "Entrada regular", 5000))
        cursor.execute('INSERT INTO tipoEntrada (nombre, descripcion, precio) VALUES (?, ?, ?)', ("vip", "Entrada VIP", 10000))
        cursor.execute('INSERT INTO formaPago (nombre, descripcion) VALUES (?, ?)', ("efectivo", "Pago en efectivo"))
        cursor.execute('INSERT INTO formaPago (nombre, descripcion) VALUES (?, ?)', ("tarjeta", "Pago con tarjeta"))
        conn.commit()
    finally:
        conn.close()

    if db_exists:
        # Si la DB ya existía, informamos (no creamos otra copia)
        # Esto evita confusión cuando se ejecuta el proyecto desde distintos CWDs.
        print(f"Usando base de datos existente en: {DB_PATH}")
    else:
        print(f"Base de datos creada en: {DB_PATH}")


def get_or_create_usuario(email: str) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT id FROM usuario WHERE email = ?', (email,))
        row = cur.fetchone()
        if row:
            return row['id']
        cur.execute('INSERT INTO usuario (email) VALUES (?)', (email,))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_or_create_forma_pago(nombre: str, descripcion: Optional[str]) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT id FROM formaPago WHERE nombre = ?', (nombre,))
        row = cur.fetchone()
        if row:
            return row['id']
        cur.execute('INSERT INTO formaPago (nombre, descripcion) VALUES (?, ?)', (nombre, descripcion))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_or_create_tipo_entrada(nombre: str, descripcion: Optional[str], precio: float) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT id FROM tipoEntrada WHERE nombre = ? AND precio = ?', (nombre, precio))
        row = cur.fetchone()
        if row:
            return row['id']
        cur.execute('INSERT INTO tipoEntrada (nombre, descripcion, precio) VALUES (?, ?, ?)', (nombre, descripcion, precio))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
def get_tipo_entrada_por_nombre(nombre: str):
    """
    Busca en la tabla tipoEntrada por nombre y devuelve una instancia de TipoEntrada
    (importada dinámicamente para evitar problemas de import circular).
    Devuelve None si no se encuentra.
    """
    if not nombre:
        return None

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('SELECT nombre, descripcion, precio FROM tipoEntrada WHERE nombre = ?', (nombre,))
        row = cur.fetchone()
        if not row:
            return None

        # Import dinámico del modelo para no forzar import al cargar el módulo
        try:
            from modelos.tipoEntrada import TipoEntrada
        except Exception:
            # Si no existe el modelo, devolver un dict como fallback
            return {
                "nombre": row['nombre'],
                "descripcion": row['descripcion'],
                "precio": float(row['precio'])
            }

        return TipoEntrada(nombre=row['nombre'], descripcion=row['descripcion'], precio=float(row['precio']))
    finally:
        conn.close()


def insertar_entrada(usuario_email: str, cantidad: int, fecha_visita: str, forma_pago_nombre: str, forma_pago_descripcion: Optional[str], fecha_compra: str, estado_pago: str) -> int:
    """Inserta una entrada y devuelve su id."""
    usuario_id = get_or_create_usuario(usuario_email)
    forma_pago_id = get_or_create_forma_pago(forma_pago_nombre, forma_pago_descripcion)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO entrada (usuario_id, cantidad, fecha_visita, forma_pago_id, fecha_compra, estado_pago) VALUES (?, ?, ?, ?, ?, ?)',
            (usuario_id, cantidad, fecha_visita, forma_pago_id, fecha_compra, estado_pago)
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def insertar_detalle(entrada_id: int, edad_visitante: int, tipo_entrada_nombre: str, tipo_entrada_descripcion: Optional[str], tipo_entrada_precio: float) -> int:
    tipo_id = get_or_create_tipo_entrada(tipo_entrada_nombre, tipo_entrada_descripcion, tipo_entrada_precio)
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO detalleEntrada (edad_visitante, tipo_entrada_id, entrada_id) VALUES (?, ?, ?)', (edad_visitante, tipo_id, entrada_id))
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()



# Inicializar la DB al importar este módulo (seguro y idempotente)
init_db()




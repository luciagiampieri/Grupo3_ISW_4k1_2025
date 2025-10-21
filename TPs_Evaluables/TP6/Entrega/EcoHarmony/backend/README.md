# Estructura del proyecto

El backend de EcoHarmony está desarrollado en Python, siguiendo una arquitectura modular orientada a objetos. Su objetivo principal es gestionar las operaciones del sistema de ventas de entradas y control de usuarios para el parque/zoo ecológico.

backend/
│
├── api.py                 # Define los endpoints REST del sistema
├── app.py                 # Punto de entrada principal del backend
├── base_de_datos.py       # Configuración y conexión con la base de datos SQLite
├── ecoharmony.db          # Base de datos local del proyecto
├── package-lock.json      # Dependencias de entorno (si aplica con Node para testing)
├── test_compra.py         # Pruebas unitarias para el proceso de compra
│
└── modelos/               # Carpeta con las clases de dominio
    ├── detalleEntrada.py  # Modelo de detalle de entradas
    ├── entrada.py         # Modelo principal de entradas
    ├── formaPago.py       # Modelo de métodos de pago
    ├── tipoEntrada.py     # Modelo de tipos de entrada (niños, adultos, etc.)
    ├── usuario.py         # Modelo de usuario del sistema
    └── __pycache__/       # Puede estar o no. Archivos compilados automáticamente por Python

# Observaciones técnicas

El backend utiliza SQLite como base de datos embebida (ecoharmony.db), ideal para entorno local o pruebas.

El archivo api.py implementa la API RESTful, gestionando operaciones CRUD sobre los modelos.

### app.py actúa como orquestador, inicializando la aplicación y exponiendo las rutas. (hay que corregir, porque actualmente solo hay un envío de mail).

test_compra.py incluye pruebas unitarias que validan el proceso de compra, verificando la correcta interacción entre modelos y base de datos.

Se recomienda mantener las dependencias actualizadas y, en caso de desplegar el sistema, migrar la base de datos a un motor más robusto (por ejemplo, PostgreSQL o MySQL).
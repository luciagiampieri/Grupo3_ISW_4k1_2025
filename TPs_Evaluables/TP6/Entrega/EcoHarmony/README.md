# 🌱 EcoHarmony

**EcoHarmony** es una aplicación web desarrollada como trabajo práctico para la materia *Ingeniería de Software* (UTN – 4° año, 2025).  
El proyecto combina un **backend en Python (Flask)** y un **frontend en React (Vite)** para gestionar la compra de entradas a eventos ecológicos, simulando una pasarela de pago tipo *MercadoPago*.

---

## ⚙️ Estructura del proyecto

EcoHarmony/
├── backend/ # API, base de datos y lógica del servidor
│ ├── modelos/ # Modelos de datos (usuario, entrada, etc.)
│ ├── app.py # Punto de entrada principal del backend
│ ├── api.py # Endpoints del sistema
│ ├── base_de_datos.py # Configuración y conexión a SQLite
│ ├── ecoharmony.db # Base de datos local
│ └── test_compra.py # Tests del backend
│
└── frontend/ # Interfaz visual (React + Vite)
├── src/ # Código fuente de la aplicación
├── public/ # Archivos estáticos
├── package.json # Dependencias y scripts del frontend
└── vite.config.js # Configuración de Vite

---

### 🔧 Requisitos
- Python 3.12 o superior  
- pip (administrador de paquetes)

### 🚀 Instalación y ejecución

1. Abrir una terminal en la carpeta `backend/`
2. Instalar dependencias:
    >>> pip install flask flask-cors
3. Ejecutar la app
    >>> python app.py

4. Abrir una terminal en la carpeta `backend/`
5. Instalar dependencias:
    >>> npm install
6. Levantar el entorno de desarrollo:
    >>> npm run dev

El sitio quedará disponible (por defecto) en http://localhost:5173

### 🧪 Testing
1. Para ejecutar los tests del backend:
    >>> pytest test_compra.py

### 🧹 Limpieza y mantenimiento
1. Ver el archivo CLEANUP.md para comandos de limpieza rápida.



-----


# React + Vite

Este proyecto utiliza el entorno React + Vite para el desarrollo del frontend de EcoHarmony, un parque que promueve la sustentabilidad y la educación ambiental.
El template base de Vite ofrece un entorno ligero y rápido, con compatibilidad para HMR (Hot Module Replacement) y reglas de ESLint integradas.

Actualmente, dos plugins oficiales están disponibles:
    @vitejs/plugin-react: usa Babel (o oxc con rolldown-vite) para Fast Refresh.
    @vitejs/plugin-react-swc: utiliza SWC para Fast Refresh con mayor rendimiento.

Nota: El compilador de React no está habilitado en esta plantilla debido a su impacto en el rendimiento de desarrollo y build.
Para habilitarlo, consultar la documentación oficial.

# Estructura del proyecto

El frontend está organizado modularmente, siguiendo buenas prácticas de separación entre componentes, estilos y recursos visuales.

frontend/
│
├── index.html             # Archivo principal del proyecto
├── package.json           # Dependencias y scripts del proyecto
├── vite.config.js         # Configuración del entorno Vite
├── README.md              # Documentación del frontend
│
├── public/                # Recursos estáticos accesibles directamente
│   ├── logo1.png
│   └── vite.svg
│
└── src/                   # Código fuente principal
    ├── App.jsx            # Componente raíz del proyecto
    ├── main.jsx           # Punto de entrada de React
    ├── index.css / App.css# Estilos globales
    │
    ├── assets/            # Imágenes y recursos visuales
    │   ├── logo.png
    │   ├── mercadopago_bg_removed_outer.png
    │   └── react.svg
    │
    └── components/        # Componentes modulares de la interfaz
        ├── FakeMercadoPago.*   # Simulación de pasarela de pago
        ├── NavBar.*            # Barra de navegación principal
        ├── NavBarMP.*          # Versión adaptada para la vista de pago
        ├── PurchaseDetail.*    # Muestra detalles de la compra
        └── SimpleForm.*        # Formulario de registro y selección de entradas

# Observaciones técnicas

El proyecto utiliza Vite como bundler, optimizando tiempos de carga y desarrollo.

Cada componente tiene su propio archivo .jsx y .css, facilitando la mantenibilidad y la lectura del código.

El componente FakeMercadoPago simula el flujo de pago, permitiendo realizar pruebas sin conexión real a una pasarela externa.

NavBar y NavBarMP gestionan la navegación principal y la vista de pago respectivamente.

Se recomienda mantener una clara separación entre componentes, recursos (assets) y estilos para garantizar la escalabilidad.

Las imágenes (logo.png, mercadopago_bg_removed_outer.png) pueden reemplazarse por versiones definitivas antes del despliegue final.



-----

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
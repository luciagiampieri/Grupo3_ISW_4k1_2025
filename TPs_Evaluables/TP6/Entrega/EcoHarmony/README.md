# 🌿 EcoHarmony

**EcoHarmony** es un proyecto desarrollado para la materia *Ingeniería de Software* (UTN – Grupo 3, 4K1 2025).  
Consiste en una aplicación web que integra un **backend en Flask (Python)** y un **frontend en React (Vite)**, destinada a gestionar la compra de entradas y pagos simulados mediante un módulo tipo MercadoPago.

---

## 📁 Estructura del proyecto

EcoHarmony/
│
├── backend/ → API REST con Flask + SQLite
│ ├── modelos/ → Clases de dominio (Entrada, Usuario, etc.)
│ └── ecoharmony.db
│
└── frontend/ → Interfaz web con React + Vite
└── src/components/ → Componentes principales

---

## 🚀 Ejecución del proyecto

### 1️⃣ Backend (Flask)
1. Abrí una terminal en la carpeta `backend`.
2. Asegurate de tener Python 3.12 o superior instalado.
3. Instalá las dependencias necesarias:
>>> pip install flask
4. Iniciá el servidor: 
>>> python api.py

La API se ejecutará en:
http://127.0.0.1:5000

### 2️⃣ Frontend (React + Vite)
1. Abrí otra terminal en la carpeta frontend.
2. Instalá las dependencias:
npm install
3. Ejecutá el servidor de desarrollo:
npm run dev
4. Accedé desde el navegador al enlace que muestra la consola (por defecto suele ser): http://localhost:5173

🧠 Tecnologías principales

    Frontend: React (Vite), HTML, CSS, JavaScript (ES6)
    Backend: Python, Flask, SQLite
    Testing: pytest (en backend)
    Control de versiones: Git / GitHub

⚙️ Notas

    El archivo ecoharmony.db contiene datos de prueba locales.
    No se requiere conexión externa a internet para el backend.
    En caso de error de conexión entre frontend y backend, verificá que ambos servidores estén corriendo simultáneamente.
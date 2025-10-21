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
# 🧹 Limpieza del proyecto – EcoHarmony

Esta guía permite eliminar archivos innecesarios o pesados que pueden generar conflictos o ralentizar la ejecución del proyecto.

---

## 🗑️ Archivos y carpetas que pueden borrarse con seguridad

### En `backend/`

- `__pycache__/` → elimina los archivos compilados de Python (`*.pyc`).

- Archivos temporales de base de datos: Si necesitás reiniciar la base, podés borrar ecoharmony.db (⚠️ elimina todos los registros).

- Archivos de pruebas antiguos: test_compra.py solo es necesario para testing, puede excluirse antes de empaquetar.

### En `frontend/`

- node_modules/ → carpeta pesada que puede regenerarse con: npm install

- Archivos de caché:

        .vite/ (si existe)
        .eslintcache o similares

- Archivos de compilación temporal (si hiciste npm run build):
        
        dist/ puede eliminarse si no se usa en producción.

## ⚙️ Limpieza rápida (Windows PowerShell)

Ejecutá desde la raíz del proyecto:

    Remove-Item -Recurse -Force backend\__pycache__, backend\modelos\__pycache__, frontend\node_modules, frontend\dist

## ✅ Recomendaciones

Hacer limpieza antes de comprimir o subir el proyecto a GitHub.

No eliminar archivos .lock mientras estés desarrollando, ya que mantienen coherencia de dependencias.

Podés regenerar todo con:
    pip install -r requirements.txt
    npm install
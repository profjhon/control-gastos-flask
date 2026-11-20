# Sistema de Control de Gastos (Flask + Python + SQLite)

Aplicación web desarrollada en Python con el microframework Flask y base de datos SQLite para el registro diario de gastos y generación de reportes descargables (CSV/Excel e impresión PDF).

## 🚀 Características Principales
- **Control de Acceso:** Inicio de sesión protegido por sesiones de Flask.
  - **Usuario:** `admin`
  - **Contraseña:** `123`
- **Gestión de Gastos:** Registro rápido con fecha, descripción y monto, además de opción para eliminar registros.
- **Generación de Reportes:** Exportación directa a formato CSV (compatible con Excel) y vista optimizada para impresión o guardado en PDF.

## ⚙️ Instalación y Funcionamiento

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/profjhon/control-gastos-flask.git](https://github.com/profjhon/control-gastos-flask.git)
   cd control-gastos-flask
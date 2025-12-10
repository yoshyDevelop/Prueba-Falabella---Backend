# Rios del Desierto - Sistema de Gestion de Clientes

## Overview
Aplicacion completa para gestionar clientes y compras, con generacion de reportes de fidelizacion.

### Proposito
Prueba tecnica que demuestra integracion con Turso (SQLite en la nube), FastAPI, y Pandas para analisis de datos.

### Estado Actual
- API REST funcional con endpoints de clientes y reportes
- Frontend con Bootstrap 5 para busqueda de clientes
- Reporte de fidelizacion en Excel usando Pandas

## Stack Tecnologico
- **Backend**: Python 3.10+, FastAPI
- **Base de Datos**: Turso (libsql) / SQLite local (fallback)
- **Analisis**: Pandas, openpyxl
- **Frontend**: HTML5, Bootstrap 5, JavaScript Vanilla

## Estructura del Proyecto
```
/
├── main.py           # API FastAPI con endpoints
├── database.py       # Configuracion conexion Turso/SQLite
├── models.py         # Modelos SQLAlchemy (DocumentType, Customer, Purchase)
├── seed.py           # Script para poblar la base de datos
├── templates/
│   └── index.html    # Interfaz de usuario Bootstrap
├── local.db          # Base de datos SQLite local (si no hay Turso)
└── replit.md         # Este archivo
```

## Endpoints API
- `GET /` - Pagina principal (HTML)
- `GET /api/customer/{doc_number}` - Buscar cliente por documento
- `GET /api/customers` - Listar todos los clientes
- `GET /api/loyalty-report` - Descargar reporte Excel de fidelizacion

## Configuracion de Credenciales Turso
La aplicacion requiere dos variables de entorno para conectar con Turso:
- `TURSO_DATABASE_URL` - URL de la base de datos (ej: libsql://mi-db.turso.io)
- `TURSO_AUTH_TOKEN` - Token de autenticacion

Sin estas credenciales, la aplicacion usa SQLite local automaticamente.

## Ejecutar Seed
```bash
python seed.py
```
Esto crea:
- 3 tipos de documento (CC, NIT, PAS)
- 2 clientes de ejemplo
- Compras que superan el umbral de fidelizacion (5,000,000)

## Umbral de Fidelizacion
El reporte de fidelizacion filtra clientes con compras del ultimo mes que superen 5,000,000 COP.

# 🏋️ Mi Gimnasio

Aplicación web hecha con **Flask** + **SQLite** para llevar el registro de
tus sesiones de gimnasio: qué máquina/ejercicio usaste, cuándo y con qué
notas.

## Estructura del proyecto

```
21-gym-app/
├── docker-compose.yaml     # Definición del servicio Docker (uso en NAS/Synology)
├── ejecutar.sh             # Script de arranque para Linux/Docker
├── ejecutar.bat            # Script de arranque para Windows
├── var.env                 # Variables de entorno (puerto, ruta de la BD, debug)
└── src/
    ├── app.py              # Lógica de la app: rutas Flask, acceso a la BD SQLite
    ├── requirements.txt    # Dependencias Python (Flask)
    └── templates/
        ├── base.html           # Plantilla base (menú, estilos)
        ├── index.html          # Página de inicio con últimas actividades
        ├── maquinas.html       # Listado de máquinas/ejercicios
        ├── nueva_maquina.html  # Formulario para añadir una máquina
        ├── registrar.html      # Formulario para registrar una actividad
        └── progreso.html       # Histórico/progresión de una máquina
```

> Nota: `src/app (2).py` es una variante de trabajo (con campos de
> repeticiones/peso/series) que no está en uso; el punto de entrada actual
> es `src/app.py`.

### Modelo de datos (SQLite)

**Tabla `maquinas`** — catálogo de máquinas/ejercicios

| Columna          | Tipo    | Descripción                 |
|------------------|---------|------------------------------|
| id               | INTEGER | Clave primaria               |
| nombre           | TEXT    | Nombre único de la máquina   |
| grupo_muscular   | TEXT    | Ej: Pecho, Espalda, Piernas  |

**Tabla `registros`** — actividades registradas

| Columna     | Tipo    | Descripción                          |
|-------------|---------|----------------------------------------|
| id          | INTEGER | Clave primaria                         |
| maquina_id  | INTEGER | Referencia a `maquinas.id` (cascada al borrar) |
| fecha       | TEXT    | Fecha y hora del registro              |
| notas       | TEXT    | Notas de la actividad (obligatorias)   |

Las tablas se crean automáticamente la primera vez que arranca la
aplicación; no hace falta ejecutar ninguna migración a mano.

## Configuración

La app lee su configuración de variables de entorno, definidas en
[var.env](var.env):

| Variable        | Descripción                                      |
|-----------------|---------------------------------------------------|
| `APP_PORT_GYM`  | Puerto en el que escucha Flask                     |
| `RUTA_BD_GYM`   | Ruta al fichero SQLite de la base de datos         |
| `DEBUG`         | Modo debug (no usada actualmente por `app.py`)     |
| `SECRET_KEY`    | Clave secreta de Flask (necesaria para `flash`); no está definida en `var.env`, hay que añadirla |

Antes de arrancar, comprueba que `RUTA_BD_GYM` apunta a una ruta válida y
que el proceso tiene permisos de escritura sobre ella (el fichero de la
base de datos se crea solo si no existe).

## Instalación y ejecución en local

Requisitos: Python 3 y `pip`.

1. Instala las dependencias:

   ```bash
   pip install -r src/requirements.txt
   ```

2. Define las variables de entorno (o cárgalas desde `var.env`) y arranca
   la app:

   **Windows:**
   ```bat
   ejecutar.bat
   ```

   **Linux/macOS:**
   ```bash
   export APP_PORT_GYM=5012
   export RUTA_BD_GYM=./gym.db
   export SECRET_KEY=cambia-esto
   python src/app.py
   ```

3. Abre el navegador en `http://localhost:<APP_PORT_GYM>` (por defecto,
   `5012` según `var.env`).

## Ejecución con Docker

El [docker-compose.yaml](docker-compose.yaml) está pensado para un NAS
Synology (usa `network_mode: host` y rutas de volumen tipo
`/volume1/informatica/...`); adapta las rutas de `volumes:` y `env_file:`
a tu entorno antes de levantarlo.

```bash
docker compose up
```

El contenedor usa la imagen `python:3.14-slim`, instala `tzdata` y las
dependencias de `src/requirements.txt`, y ejecuta [ejecutar.sh](ejecutar.sh),
que a su vez lanza `python app.py`.

## Funcionalidades

- Registrar actividades (máquina + notas) desde `/registrar`.
- Gestionar el catálogo de máquinas/ejercicios (`/maquinas`, alta y baja).
- Ver las últimas actividades y totales en la página de inicio (`/`).
- Consultar el histórico/progresión de una máquina concreta
  (`/progreso/<id>`).

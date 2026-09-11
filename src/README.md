# Mi Gimnasio - App web de seguimiento de entrenamientos

Aplicación web hecha con **Flask** + **SQLite** para registrar tus sesiones de
gimnasio: qué máquina/ejercicio usaste, cuántas repeticiones, series y con
qué peso.

## Cómo ejecutarla

1. Instala las dependencias (solo Flask):

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta la aplicación:

   ```bash
   python3 app.py
   ```

3. Abre tu navegador en: http://localhost:5000

La primera vez que arranca, se crea automáticamente el archivo `gym.db`
(la base de datos SQLite) con las tablas necesarias — no necesitas hacer
nada más.

## Estructura del proyecto

```
gym_app/
├── app.py                 # Lógica de la app: rutas, conexión a la BD
├── gym.db                 # Base de datos SQLite (se crea sola al arrancar)
├── requirements.txt        # Dependencias
└── templates/
    ├── base.html            # Plantilla base (menú, estilos)
    ├── index.html           # Página de inicio con últimas actividades
    ├── maquinas.html        # Listado de máquinas
    ├── nueva_maquina.html   # Formulario para añadir una máquina
    ├── registrar.html       # Formulario para registrar reps/peso
    └── progreso.html        # Histórico de una máquina concreta
```

## Modelo de datos (SQLite)

**Tabla `maquinas`**
| Columna         | Tipo    | Descripción                  |
|-----------------|---------|-------------------------------|
| id              | INTEGER | Clave primaria                |
| nombre          | TEXT    | Nombre único de la máquina    |
| grupo_muscular  | TEXT    | Ej: Pecho, Espalda, Piernas   |

**Tabla `registros`**
| Columna       | Tipo    | Descripción                       |
|---------------|---------|-------------------------------------|
| id            | INTEGER | Clave primaria                      |
| maquina_id    | INTEGER | Referencia a `maquinas.id`          |
| fecha         | TEXT    | Fecha y hora del registro           |
| notas         | TEXT    | Notas de la actividad (obligatorias)|

## Ideas para seguir practicando y mejorar la app

- Añadir gráficos de progresión de peso a lo largo del tiempo (con
  `matplotlib` o `Chart.js`).
- Añadir un sistema de usuarios (login) si varias personas van a usarla.
- Calcular automáticamente el "1RM estimado" (repetición máxima) con
  fórmulas como la de Epley.
- Exportar el historial a CSV o Excel.
- Añadir validación más estricta en el backend (por ejemplo, con Flask-WTF).

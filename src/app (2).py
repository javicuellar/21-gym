"""
Aplicación web de seguimiento de entrenamientos de gimnasio.

Tecnologías:
- Flask: framework web ligero de Python.
- SQLite: base de datos, se guarda en un solo archivo (gym.db).

Estructura de datos:
- Tabla "maquinas": catálogo de máquinas/ejercicios (nombre, grupo muscular).
- Tabla "registros": cada serie que haces (máquina, repeticiones, peso, fecha).
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os




app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
RUTA_BD_GYM = os.environ.get("RUTA_BD_GYM")


def get_db_connection():
    """
    Abre una conexión a la base de datos SQLite.
    row_factory = sqlite3.Row nos permite acceder a las columnas
    por nombre (fila["nombre"]) en lugar de solo por índice (fila[0]).
    """
    conn = sqlite3.connect(RUTA_BD_GYM)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # activa las claves foráneas
    return conn


def init_db():
    """
    Crea las tablas si no existen todavía.
    Se llama una vez al arrancar la aplicación.
    """
    conn = get_db_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS maquinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            grupo_muscular TEXT
        );

        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maquina_id INTEGER NOT NULL,
            repeticiones INTEGER NOT NULL,
            peso REAL NOT NULL,
            series INTEGER NOT NULL DEFAULT 1,
            fecha TEXT NOT NULL,
            notas TEXT,
            FOREIGN KEY (maquina_id) REFERENCES maquinas (id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# RUTAS (endpoints) de la aplicación
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Página principal: muestra las últimas actividades registradas."""
    conn = get_db_connection()
    registros = conn.execute(
        """
        SELECT registros.id, registros.repeticiones, registros.peso,
               registros.series, registros.fecha, registros.notas,
               maquinas.nombre AS maquina_nombre,
               maquinas.grupo_muscular
        FROM registros
        JOIN maquinas ON registros.maquina_id = maquinas.id
        ORDER BY registros.fecha DESC, registros.id DESC
        LIMIT 20
        """
    ).fetchall()
    total_maquinas = conn.execute("SELECT COUNT(*) FROM maquinas").fetchone()[0]
    total_registros = conn.execute("SELECT COUNT(*) FROM registros").fetchone()[0]
    conn.close()
    return render_template(
        "index.html",
        registros=registros,
        total_maquinas=total_maquinas,
        total_registros=total_registros,
    )


@app.route("/maquinas")
def listar_maquinas():
    """Lista todas las máquinas/ejercicios del catálogo."""
    conn = get_db_connection()
    maquinas = conn.execute("SELECT * FROM maquinas ORDER BY nombre").fetchall()
    conn.close()
    return render_template("maquinas.html", maquinas=maquinas)


@app.route("/maquinas/nueva", methods=["GET", "POST"])
def nueva_maquina():
    """Formulario para añadir una máquina/ejercicio nuevo al catálogo."""
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        grupo_muscular = request.form.get("grupo_muscular", "").strip()

        if not nombre:
            flash("El nombre de la máquina es obligatorio.", "error")
            return redirect(url_for("nueva_maquina"))

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO maquinas (nombre, grupo_muscular) VALUES (?, ?)",
                (nombre, grupo_muscular),
            )
            conn.commit()
            flash(f'Máquina "{nombre}" añadida correctamente.', "success")
        except sqlite3.IntegrityError:
            flash(f'Ya existe una máquina llamada "{nombre}".', "error")
        finally:
            conn.close()

        return redirect(url_for("listar_maquinas"))

    return render_template("nueva_maquina.html")


@app.route("/maquinas/<int:maquina_id>/eliminar", methods=["POST"])
def eliminar_maquina(maquina_id):
    """Elimina una máquina y, en cascada, sus registros asociados."""
    conn = get_db_connection()
    conn.execute("DELETE FROM maquinas WHERE id = ?", (maquina_id,))
    conn.commit()
    conn.close()
    flash("Máquina eliminada.", "success")
    return redirect(url_for("listar_maquinas"))


@app.route("/registrar", methods=["GET", "POST"])
def registrar_actividad():
    """Formulario para registrar una actividad: máquina, repeticiones y peso."""
    conn = get_db_connection()
    maquinas = conn.execute("SELECT * FROM maquinas ORDER BY nombre").fetchall()

    if request.method == "POST":
        maquina_id = request.form.get("maquina_id")
        repeticiones = request.form.get("repeticiones")
        peso = request.form.get("peso")
        series = request.form.get("series") or 1
        notas = request.form.get("notas", "").strip()

        errores = []
        if not maquina_id:
            errores.append("Selecciona una máquina.")
        if not repeticiones or int(repeticiones) <= 0:
            errores.append("Las repeticiones deben ser un número mayor que 0.")
        if peso is None or peso == "" or float(peso) < 0:
            errores.append("El peso debe ser un número válido (puede ser 0).")

        if errores:
            for e in errores:
                flash(e, "error")
            conn.close()
            return redirect(url_for("registrar_actividad"))

        conn.execute(
            """
            INSERT INTO registros (maquina_id, repeticiones, peso, series, fecha, notas)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                maquina_id,
                int(repeticiones),
                float(peso),
                int(series),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                notas,
            ),
        )
        conn.commit()
        conn.close()
        flash("Actividad registrada con éxito.", "success")
        return redirect(url_for("index"))

    conn.close()
    return render_template("registrar.html", maquinas=maquinas)


@app.route("/registros/<int:registro_id>/eliminar", methods=["POST"])
def eliminar_registro(registro_id):
    """Elimina un registro de actividad concreto."""
    conn = get_db_connection()
    conn.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
    flash("Registro eliminado.", "success")
    return redirect(url_for("index"))


@app.route("/progreso/<int:maquina_id>")
def progreso_maquina(maquina_id):
    """Muestra el histórico de una máquina concreta, para ver la progresión."""
    conn = get_db_connection()
    maquina = conn.execute(
        "SELECT * FROM maquinas WHERE id = ?", (maquina_id,)
    ).fetchone()
    registros = conn.execute(
        """
        SELECT * FROM registros
        WHERE maquina_id = ?
        ORDER BY fecha ASC
        """,
        (maquina_id,),
    ).fetchall()
    conn.close()

    if maquina is None:
        flash("Esa máquina no existe.", "error")
        return redirect(url_for("listar_maquinas"))

    return render_template("progreso.html", maquina=maquina, registros=registros)


if __name__ == "__main__":
    init_db()

    # debug=True recarga el servidor automáticamente al guardar cambios.
    # app.run(host="0.0.0.0", port=5000, debug=True)
    APP_PORT_GYM = os.environ.get("APP_PORT_GYM")
    app.run(port=APP_PORT_GYM)

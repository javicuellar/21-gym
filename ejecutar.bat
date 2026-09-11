echo off

:: ══════════════════════════════════════════════
::  SCRIPT DE ARRANQUE — 21-gym_app
:: ══════════════════════════════════════════════
::
:: Autor: Javier C.
:: Fecha: 2026-07-18

:: Leer las variables de entorno desde el archivo var.env
for /f "usebackq tokens=1,* delims==" %%A in ("E:\\Python\\config\\DES\\var.env") do (
    set "%%A=%%B"
    )

::  Ejecuatar aplicación Flask para gestionar contactos
echo Arrancando Appweb Contactos...
echo     Base de datos : %RUTA_BD_GYM%
echo     Puerto        : %APP_PORT_GYM%
echo --------------------------------------------------------------------------

python ./src/app.py

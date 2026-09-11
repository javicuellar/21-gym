#!/bin/bash
# ══════════════════════════════════════════════
#  SCRIPT DE ARRANQUE — 21-gym_app
# ══════════════════════════════════════════════
#
# Autor: Javier C.
# Fecha: 2026-07-18

# Actualizar e instalar tzdata para evitar problemas con la zona horaria
apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

# Timezone (override with TZ env var)
export TZ=Europe/Madrid
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# instalar dependencias de Python
cd src
pip install --no-cache-dir -r ./requirements.txt

set -e

echo "  Arrancando Aplicación Gym_app ..."
echo "    Base de datos : $RUTA_BD_GYM"
echo "    Puerto        : $APP_PORT_GYM"
echo ""

python app.py

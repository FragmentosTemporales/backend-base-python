#!/bin/sh

set -e  # Hacer que el script salga en caso de un comando falle

echo "---------------------------------------------"
echo "|           Iniciando Instalación           |"
echo "---------------------------------------------"
docker compose run --rm scripts sh -c "python manage.py install"
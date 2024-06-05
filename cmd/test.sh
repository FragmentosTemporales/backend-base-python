#!/bin/sh
echo "---------------------------------------------"
echo "|            Iniciando Testing              |"
echo "---------------------------------------------"
docker compose run --rm scripts sh -c "python manage.py test && flake8"

if [ -f "scripts/test.db" ]; then
  rm "scripts/test.db"
  echo "---------------------------------------------"
  echo "|  Archivo test.db eliminado exitosamente   |"
  echo "---------------------------------------------"
else
  echo "---------------------------------------------"
  echo "|     Archivo test.db no encontrado         |"
  echo "---------------------------------------------"
fi

echo "---------------------------------------------"
echo "|                 Finalizando               |"
echo "---------------------------------------------"
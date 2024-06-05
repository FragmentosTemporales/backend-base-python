#!/bin/sh

set -e  # Hacer que el script salga en caso de un comando falle

print_header() {
  echo "---------------------------------------------"
  echo "| $1"
  echo "---------------------------------------------"
}

run_command() {
  description=$1
  shift
  print_header "$description"
  docker compose run --rm scripts sh -c "$@"
}

print_header "         Iniciando Base de Datos           "
run_command "Iniciando Base de Datos" "python manage.py db init"

print_header "          Migrando Base de Datos           "
run_command "Migrando Base de Datos" "python manage.py db migrate"

print_header "       Actualizando Base de Datos          "
run_command "Actualizando Base de Datos" "python manage.py db upgrade"

print_header "              Creando Admin                "
run_command "Creando Admin" "python manage.py create-user --email admin@admin.com --password admin"

print_header "USER : admin@admin.com                    "
print_header "PASS : admin                              "
print_header "                Finalizando                "
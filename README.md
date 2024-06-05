# Risk Management - Backend 


## 1. Instalación

Para descargar la aplicación del repo, se debe escribir el siguiente comando:

```
$ git clone https://github.com/FragmentosTemporales/risk-management
```

### Variables de entorno

Al interior de la carpeta /Sripts debes crear un documento env.env el cual debe contener las siguiente variables, puedes guiarte con el documento example.env :

```
FLASK_ENV=dev

JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_EXPIRES_HOURS=
JWT_ACCESS_TOKEN_EXPIRES_DAYS=
SECRET_KEY=

POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
```

En este repositorio en particular, incluyo valores de variables que *DEBEN* coincidir con el docker-compose.yml

### Instalación de Docker Compose

Para instalar la aplicación debes ejecutar el siguiente código, es necesario que las variables de entorno estén definidas para este punto:

```
$ docker compose build
```

## 2. Ejecución

Para ejecutar la aplicación debes ingresar el siguiente comando:

```
$ docker compose up
```

## 3.- ¿Qué podemos ejecutar?

En el archivo *manage.py* podrás encontrar comandos por consola. Una vez hayas iniciado la aplicación deberás vincularla a la base de datos:

```
$ docker compose run --rm scripts sh -c "python manage.py db init"
```

Luego deberás migrar:

```
$ docker compose run --rm scripts sh -c "python manage.py db migrate"
```

Para finalmente upgradear:

```
$ docker compose run --rm scripts sh -c "python manage.py db upgrade"
```

<hr/>

Comandos para ejecutar Scripts:

Iniciar Testing:
```
sh cmd/test.sh
```
Iniciar Base de Datos:
```
sh cmd/init_db.sh
```

<hr/>



En estos momentos debes tener tu base de datos enlazada a tu aplicación, si es que quieres probar esto puedes ejecutar el siguiente comando:

```
$ docker compose run --rm scripts sh -c "python manage.py create-user --email example@mail.com --password 123456"
```

En caso de estar funcionando todo correctamente debería retornar un mensaje tipo:

*"Usuario guardado correctamente"*

También puedes probar la función para crear el usuario a través del endpoint:

```
http://localhost:4000/register
```

Enviando un objeto JSON como el siguiente:

```
{
	"email": "example@mail.com",
	"password": "123456"
}
```

### ¿Y los testeos?

Si ya llegaste a este punto, podemos hablar de testeos.
Esta aplicación tiene desarrollados testeos para ciertos modelos, los cuales puedes ejecutar a través de la consola con el siguiente comando:

```
$ docker compose run --rm scripts sh -c "python manage.py test"
```

*IMPORTANTE*

No sólo podrás ejecutar los testeos, esta función también incluye flake8, un corrector de sintáxis diseñado para python, podrás ejecutarlo con el siguiente código:

```
$ docker compose run --rm scripts sh -c "python manage.py test && flake8"
```

<hr/>

## 4.- Bibliografía

A continuación te dejo el link con la documentación de Flask, específicamente la versión utilizada en este repositorio.

```
https://flask.palletsprojects.com/en/2.3.x/
```

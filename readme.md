# API SALUD-PUBLICA

Este repositorio contiene la API usada en la aplicacion de salud-publica

### To-do
- Cambiar el front para que envie el asunto y dirección de correo
- Definir si usar django-test o pruebas automaticas con selenium

#### Despliegue en Heroku
Primero guarda tus cambios:\
`$ git commit -am "Guardar ultimos cambios`\
Para enviar la rama master a Heroku usa:\
`$ git push heroku master`\
Para enviar cualquier otra rama a Heroku usa:\
`$ git push heroku nombrerama:master`

#### Despliegue del front end
Primero se debe compilar el front para el deployment en GCP usando:\
`$ npm run build`\
Luego de compilar los archivos para el deployment usa:\
`$ gcloud app deploy`

#### Despliegue de la API en Google Cloud
Enviar los ultimos cambios de la rama para google cloud a git:\
`$git commit -am "Guardar ultimos cambios"`\
`$git push origin computeEngine-deployment`\
En la maquina virtual de google cloud, traer los ultimos cambios:\
`$git fetch origin`\

Ver los paquetes de python instalados en el venv:\
`$sudo pip freeze`\
Instalar las variables de entorno necesaria para que la API funcione:\
`$source  ./envVars.sh`\
Actualiza las variables de entorno del archivo .env y luego has push de la rama\
y recuerda siempre que la maquina virtual no levanta la api en la dirección 127.0.0.1\
por lo cual para poder correr la app de django debes usar la dirección 0.0.0.0.

Conectarme por terminar de linux a la instancia de compute engine de la api\
`$ gcloud compute ssh saludpublica-api --project salud-publica-puj --zone us-central1-a`\

Correr el script sin perder el terminal:\
`$ nohup sudo python3 manage.py runserver 0.0.0.0:8000`\

Usar gunicorn para servir la aplicación:\
`$ sudo gunicorn --bind 0.0.0.0:8000 salud_publica.wsgi`

Despliega la app en el background con gunicorn
`$ sudo gunicorn --config dev.py salud_publica.wsgi`

Rastrea los logs que va dejando tu aplicación 
`$ sudo tail -f /var/log/gunicorn/dev.log`

Cuando necesites parar gunicorn usa:
`$ pkill gunicorn`


Continue reading these posts:
-https://realpython.com/django-nginx-gunicorn/
-https://www.digitalocean.com/community/tutorials/como-configurar-django-con-postgres-nginx-y-gunicorn-en-ubuntu-18-04-es
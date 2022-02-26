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

#### Despliegue del front end en Google Cloud
Primero se debe compilar el front para el deployment en GCP usando:\
`$ npm run build`\
Luego de compilar los archivos para el deployment usa:\
`$ gcloud app deploy`

## Despliegue de la API en Google Cloud
Enviar los ultimos cambios de la rama para google cloud a git:\
`$git commit -am "Guardar ultimos cambios"`\
`$git push origin computeEngine-deployment`\
En la maquina virtual de google cloud, traer los ultimos cambios:\
`$git fetch origin`\
Ver los paquetes de python instalados en el venv:\
`$sudo pip freeze`\
Conectarme por terminar de linux a la instancia de compute engine de la api\
`$ gcloud compute ssh saludpublica-api --project salud-publica-puj --zone us-central1-a`

Despliega la app en el background con gunicorn\
`$ sudo gunicorn --config dev.py salud_publica.wsgi`

Rastrea los logs que va dejando tu aplicación\
`$ sudo tail -f /var/log/gunicorn/dev.log`

Cuando necesites parar gunicorn usa:\
`$ pkill gunicorn`

Debido a que usas una llave de deployment de github para traer los cambios
a la maquina virtual de Google, recuerda usar los siguientes comandos para
poder usar git pull sin errores:\
`$ eval ssh-agent`\
`$ ssh-add ~/.ssh/id_rsa`\
`$ git pull`

## Cuando quieras borrar todo
Como recordaras es usual que tengas que borrar todo e iniciar desde cero
por lo cual aqui te van unos tips de como lograrlo:
- Conectate por medio de psql a la BD `$ psql -h 34.135.94.2 -U postgres postgres`
- Luego borrale y vuelve la a crear usando `$ DROP DATABASE "mydb";` y luego `$ CREATE DATABASE mydb`
- Si la borras te recuerdo que ya no tienes un dispositivo con 2FA por lo cual debes ir los urls principales y comentar la linea
de admin site que usa OTP auth


Continue reading these posts:
- https://realpython.com/django-nginx-gunicorn/
- https://www.digitalocean.com/community/tutorials/como-configurar-django-con-postgres-nginx-y-gunicorn-en-ubuntu-18-04-es
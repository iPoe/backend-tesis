# API SALUD-PUBLICA

Este repositorio contiene la API usada en la aplicacion de salud-publica

### To-do
- Agregar la funcionalidad de subir audio de llamada
- Agregar funcionalidad de envio de correo masivo
- Cambiar el front para que envie el asunto y dirección de correo
- Agregar manual para hacer deploy en Heroku
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
`$ gcloud app deploy`\
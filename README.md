# Entrega 3
Team: Cloudians 

## Tabla de contenido
- [Pre-requisitos para cada microservicio](#pre-requisitos-para-cada-microservicio)
- [Estructura de cada microservicio](#estructura-de-cada-microservicio)
  - [Archivos de soporte](#archivos-de-soporte)
  - [Carpeta src](#carpeta-src)
  - [Carpeta test](#carpeta-test)
- [Ejecutar un microservicio](#ejecutar-un-microservicio)
  - [Instalar dependencias](#instalar-dependencias)
  - [Variables de entorno](#variables-de-entorno)
  - [Ejecutar el servidor](#ejecutar-el-servidor)
  - [Ejecutar pruebas](#ejecutar-pruebas)
  - [Ejecutar desde Dockerfile](#ejecutar-desde-dockerfile)
- [Ejecutar Docker Compose](#ejecutar-docker-compose)
- [Ejecutar Colección de Postman](#ejecutar-colección-de-postman)
- [Ejecutar evaluador github action workflow](#ejecutar-evaluador-github-action-workflow)
- [Ejecución Entrega 2](#Ejecución-Entrega-2)

## Pre-requisitos para cada microservicio
- Python ~3.9
- pip
- Docker
- Docker-compose
- Postman
- PostgreSQL
    - Las instrucciones pueden variar según el sistema operativo. Consulta [la documentación](https://www.postgresql.org/download/). Si estás utilizando un sistema operativo basado en Unix, recomendamos usar [Brew](https://wiki.postgresql.org/wiki/Homebrew).


## Estructura de cada microservicio
Cada microservicio utiliza Python y FastAPI para ejecutar el servidor, y pytest para llevar a cabo las pruebas unitarias. Todos los microservicios comparten una estructura común. A continuación, se presenta un esqueleto que describe la estructura general de los microservicios implementados:

- cloud-functions
  - polling-function
  - email-function
- collections
- creditcards
- deployment
- entrega2
- legacy
  - posts-legacy
  - routes-legacy
  - users-legacy
- newman-envs
- offers
- posts
- routes
- users
- utility
- Pipfile
- Pipfile.lock
- README.md
- config.yaml
- docker-compose.yml


En esta estructura se reflejan todos los archivos de los microservicios y demas nesecitados para la entrega 3. En este caso los folders como creditcards, offers, posts, routes, entrega2, users, utility representan los servicios usados. Especificamente para la entrega 3 se creo el nuevo serivico de creditcards. Para guardar los yaml correspondientes a los deployments se tiene todos los archivos guarados en el folder de deployments. Adicionalmente en la carpeta de cloud functions se tiene el contendido de dos cloud functions, email-function y polling function las cuales son requeridas para la entrega 3. 

### Archivos de soporte
- `requirements.txt`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. Consulta la sección **Instalar dependencias**.
- `.env.example`: Archivo de plantilla Env utilizado para definir variables de entorno. Consulte la sección  **Variables de entorno**.
- `.env`: Archivo utilizado para definir variables de entorno para las pruebas unitarias. Consulta la sección **Variables de entorno**.
- Dockerfile: Definición para construir la imagen Docker del microservicio. Consulta la sección **Ejecutar desde Dockerfile**.
- docker-compose.yml: Define una base de datos de prueba para el microservicio, un contendor de prueba para probar con el servicio user y su base de datos de prueba respectiva. Consultar la seccion **Ejecutar desde Docker**

Cada microservicio tiene sus propios archivos de dependencia incluidos los cuales caen en alguna de las anteriores categorias.

## Ejecutar un microservicio
### Instalar dependencias
Para gestionar nuestras dependencias usamos virtual enviroments de python. Para declarar las dependencias del microservicio se uso un archivo de `requirements.txt` con el cual se puede genrar el ambiente virtual de tal manera que 
se cree una carpeta con todo el ambiente virtual con el nombre de venv. Como pre requisito se tiene que tener pip instalado.

Comando de instalacion de virtual enviroments
```bash
$> pip install virtualenv
``` 

Crear un nuevo virtual enviroment llamado venv
```bash
$> virtualenv venv
```
Activa el ambiente virtual (Win,Linux,Mac)
```bash
windows >  venv\Scripts\activate
linux/mac > source venv/bin/activate
```

Instalar requirements

```bash
$>  pip install -r requirements.txt 
```

## Montar la infraestructura con kubernetes

En la carpeta de deployments se puede encontrar todos los yaml relacionados a los deployments de Kubernetes que se realizaron para la entrega 3. 
Asumiendo que ya se tiene un cluster generado en GCP lo que se debe hacer es primero correr el base layer deployment, new services deployment, true native deployment, componentes entrega 3 deployment, ingress deployment. 

Orden de despliegue de k8:
1. k8s-base-layer-deployment.yaml
2. k8s-new.services.deployment.yaml
3. k8s-true-native-deployment.yaml
4. k8s-new-services-deployment.yaml

## Direccion del ingress

El proyecto actual tiene la direccion del ingres en la siguiente ruta IP: 34.149.221.138

## Ejecutar Colección de Postman
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Collecion de pruebas:
- Entrega 3: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/monitor-202314/main/entrega3/entrega3.json

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

# Ejecución Entrega 3
En este caso se puede utilizar la seccion anterior que describe como desplegar la infraestructura de kubernetes para hacer el despliegue y montarlo en GCP. Adicionalmente se aconseja descargar las colecciones de pruebas de postmans para la entrega 3.



--REVISION

El archivo ci_pipeline.yaml contiene la configuración para el proceso de Integración Continua (CI) del proyecto; específicamente, define una serie de trabajos (Jobs) que se ejecutan automáticamente en eventos particulares, como el push de código a las ramas "main" y "develop". Uno de estos trabajos se llama test_entrega2.

El job test_entrega2 se encarga de todas las pruebas relacionadas con la segunda entrega del proyecto; aquí detallamos sus pasos específicos:

1.	Configuración del Entorno: Ejecutamos la tarea en una máquina virtual con el sistema operativo Ubuntu; en este caso, utilizamos la versión 3.9 de Python.

2.	Preparación del Entorno de Python: Configuramos la versión especificada de Python e instalamos todas las herramientas necesarias para el proyecto, garantizando así un funcionamiento sin problemas y procesos de desarrollo.

3.	Instalación de Dependencias: Nos dirigimos al directorio ./entrega2 e instalamos las dependencias del proyecto utilizando Pipenv, asegurando que todas las bibliotecas necesarias estén disponibles para las pruebas.

4.	Configuración de la Base de Datos: Instalamos una instancia de PostgreSQL en un contenedor Docker, específicamente para la Prueba de Entrega 2; establecemos las credenciales para asegurarnos de que la base de datos esté disponible antes de continuar.

5.	Ejecución de Pruebas Unitarias: Finalmente, se ejecutan las pruebas unitarias del proyecto utilizando Pytest, y posteriormente se configuran las variables de entorno como el nombre de la base de datos, el host y otras configuraciones relacionadas. Estas pruebas incluyen la medición de la cobertura del código; si la cobertura es inferior al 70%, se considera que el trabajo ha fallado.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo17/assets/56740710/351a89fd-1ecd-457d-8f54-885d10654137" alt="Screenshot" width="800">


En resumen, la función de test_entrega2 es automatizar la ejecución de las pruebas de entrega 2, asegurando que el entorno esté configurado de manera adecuada y consistente. Si la cobertura de código no alcanza un mínimo de 70%, esto indica un fallo en nuestro proceso de integración continua; estos parámetros garantizan pruebas rigurosas antes de implementar en las ramas principales del proyecto.


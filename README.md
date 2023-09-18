# Entrega 1
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

- Microservicio
  - README.md
  - LICENSE.md
  - src
    - routes
      - router.py
      - schemas.py
      - utils.py
    - constants.py
    - database.py
    - exception.py
    - main.py
    - models.py
    - schemas.py
  - tests
    - routes
      - test_router.py
    - conftest.py
  - requirements.txt
  - Dockerfile
  - docker-compose.yml

Las carpetas principales de cada microservicio son "src" y "tests". En la carpeta "src", se construye el proyecto utilizando el framework FastAPI. El archivo principal es "main.py"; sin embargo, todas las rutas se definen en el archivo "router.py", el cual se encuentra ubicado en la carpeta de nivel superior que comparte el nombre de su microservicio.

### Archivos de soporte
- `requirements.txt`: Este archivo declara todas las dependencias que serán utilizadas por el microservicio. Consulta la sección **Instalar dependencias**.
- `.env.example`: Archivo de plantilla Env utilizado para definir variables de entorno. Consulte la sección  **Variables de entorno**.
- `.env`: Archivo utilizado para definir variables de entorno para las pruebas unitarias. Consulta la sección **Variables de entorno**.
- Dockerfile: Definición para construir la imagen Docker del microservicio. Consulta la sección **Ejecutar desde Dockerfile**.
- docker-compose.yml: Define una base de datos de prueba para el microservicio, un contendor de prueba para probar con el servicio user y su base de datos de prueba respectiva. Consultar la seccion **Ejecutar desde Docker**

### Carpeta src
Esta carpeta contiene el código y la lógica necesarios para declarar y ejecutar la API del microservicio, así como para la comunicación con la base de datos. 
Todos los microservicios fueron construidos en FastAPI.

Dentro de src hay 1 carpeta principal, la cual toma el nombre del microservicio que esta siendo desarollado:
- `/<nombre_microservicio>`: Esta carpeta contiene tres archivos `router.py`, `schemas.py`, `utils.py`. 
  -  `router.py` : En el archivo se encuentran las definiciones de todas las rutas del proyecto. 
  ```python
  """ Router for routes microservice on /routes"""
    
    router = APIRouter()
    
    
    @router.post("/reset")
    async def reset(sess: Session = Depends(get_session)):
        """
        Clears route table in the db.
        :param sess: gets the current session
        :return: json -> msg: Todos los datos fueron eliminados
        """
        try:
            statement = delete(Route)
            with sess:
                sess.execute(statement)
                sess.commit()
        except Exception as e:
            logging.error(e)
            err_msg = {"msg": "Un error desconocido ha ocurrido", "error": str(e)}
            return JSONResponse(content=err_msg, status_code=500)
        return {"msg": "Todos los datos fueron eliminados"}

  ```
  - `schemas.py`: En el archivo de schemas se tienen los esquemas de pydantic para respuestas y requests que provienen del microservico.
  ```python
  class CreateUserRequestSchema(BaseModel):
    """
    Used when creating a user
    """
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    email: EmailStr = Field(min_length=1)
    phoneNumber: Optional[str] = None
    dni: Optional[str] = None
    fullName: Optional[str] = None

  ```
  - `utils.py`: Este es un archivo adjacente a router.py puesto contiene todos los metodos utilitarios y de validaciones de este. Adicionalmente ecapsula la mayoria de interacciones con la base de datos.
  ```python
  @staticmethod
    def get_route_id(route_id: str, session: Session):
        """
        Searches for a route corresponding to the given id.
        Returns the route if it exists, else it returns none
        :param session: Current session
        :param route_id: the routes uuid
        :return: Route object if it exists, else None if no result was found
        """
        try:
            found_route = session.execute(
                select(Route).where(Route.id == route_id)
            ).scalar_one()
            return found_route
        except NoResultFound:
            return None

  ```
- En la base de src adicionalmente se encuentran una variedad de archivos importantes para el funcioanmeinto del proyecto, estos son los mas importantes:
  - `database.py`: Habilita la conexión con la base de datos de postgres por medio de SQLAlchemy
  - `main.py` : El archivo principal del proyecto donde se inicializa la conexion con la base de datos y la API en si. No contiene nada de logica, ya que esta se le delega al router.
  - `models.py` : Contiene los modelos de la tabla que corresponde en la base de datos con todas sus respectivas declaraciones de tipo.
  - `schemas.py` : Contiene el esquema basico de un objeto que le corresponde a el servicio (User,Route,etc.)


### Carpeta test
Esta carpeta contiene las pruebas para los componentes principales del microservicio que han sido declarados en la carpeta `/src`. Los test se realizaron por medio de pytest.
Dentro de la carpeta de test estan dos elementos muy importantes. Primero es el archivo de conftest.py el cual crea un fixture para establecer una conexion externa con la base de datos de prueba. Adicionalmente dentro de la carpeta de <nombre_microservicio> se encuentra el archivo de test_<nombre_microservicio>.py el cual contiene todas las pruebas sobre las rutas del microservicio en cuestion.

```python
   ##ejemplo test_router

    def test_ping(
            client: TestClient,
            session: Session,
            faker
    ):
        """
    
        :param client:
        :param session:
        :param faker:
        :return:
        """
        session.execute(
            delete(Route)
        )
        session.commit()
    
        response = client.get("/routes/ping")
        assert response.status_code == 200
    
        response_body = response.text
    
        assert response_body == "pong"

  ```

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

### Variables de entorno

En nuestros servidores de FastAPI las pruebas unitarias utilizan de variables de entorno declaradas en un archivo `.env` para ser ejecutadas con el microservicio.
En estos archivos se puede encontrar información principalmente relacionada a la conexion a la base de datos.

Vale la pena mencionar que incluso si las variables de entorno declaran la conexion con la base de datos, lo que se uso principalmente para poder probar los srvicios fue el docker-compose.yml
el cual permitia configurar y prender las bases de datos y microservicios adjacentes de una forma mas rapida y confiable.

Contenido .env
- DB_USER: Usuario de la base de datos Postgres
- DB_PASSWORD: Contraseña de la base de datos Postgres
- DB_HOST: Host de la base de datos Postgres
- DB_PORT: Puerto de la base de datos Postgres
- DB_NAME: Nombre de la base de datos Postgres
- USERS_PATH: Para los microservicios que se comunican con el microservicio de Usuarios, necesitas especificar esta variable de entorno que contiene la URL utilizada para acceder a los endpoints de usuarios. (Ejemplo: http://localhost:3000, http://users-service)

Estas variables de entorno deben especificarse en `.env` y `.env.examples`.

### Ejecutar el servidor
Una vez que las variables de entorno estén configuradas correctamente, tanto en .env como en el docker-compose.yml. 
Para ejecutar el servidor se utiliza el siguiente comando:

```bash
$> uvicorn main:app --host 0.0.0.0 --port <PORT_TO_RUN_SERVER> --reload 

# Ejemplos

# Users
$> uvicorn main:app --host 0.0.0.0 --port 12001 --reload 

# Routes
$> uvicorn main:app --host 0.0.0.0 --port 12002 --reload 

# Offers
$> uvicorn main:app --host 0.0.0.0 --port 12003 --reload 

# Posts
$> uvicorn main:app --host 0.0.0.0 --port 12004 --reload 

```
### Ejecutar pruebas
Para ejecutar las pruebas unitarias de los microservicios y establecer el porcentaje mínimo de cobertura del conjunto de pruebas en 70%, ejecuta el siguiente comando:
```bash
pytest --cov-fail-under=70 --cov=src
pytest --cov-fail-under=70 --cov=src --cov-report=html
```
### Ejecutar desde Dockerfile
Para construir la imagen del Dockerfile en la carpeta, ejecuta el siguiente comando:
```bash
$> docker build . -t <NOMBRE_DE_LA_IMAGEN>
```
Y para ejecutar esta imagen construida, utiliza el siguiente comando:
```bash
$> docker run <NOMBRE_DE_LA_IMAGEN>
```

## Ejecutar Docker Compose
Para ejecutar todos los microservicios al mismo tiempo, utilizamos docker-compose para declarar y configurar cada Dockerfile de los microservicios. Para ejecutar docker-compose, utiliza el siguiente comando:
```bash
$> docker-compose -f "<RUTA_DEL_ARCHIVO_DOCKER_COMPOSE>" up --build

# Ejemplo
$> docker-compose -f "docker-compose.yml" up --build
```

## Ejecutar Colección de Postman
Para probar los servicios API expuestos por cada microservicio, hemos proporcionado una lista de colecciones de Postman que puedes ejecutar localmente descargando cada archivo JSON de colección e importándolo en Postman.

Lista de colecciones de Postman para cada entrega del proyecto:
- Entrega 1: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/monitor-202314/main/entrega1/entrega1.json
- Entrega 2: https://raw.githubusercontent.com/MISW-4301-Desarrollo-Apps-en-la-Nube/monitor-202314/main/entrega2/entrega2_verify_new_logic.json
- Entrega 3: Para esta entrega no tenemos un workflow evaluador, por lo que no se proporciona ninguna colección de Postman.

Después de descargar la colección que deseas usar, impórtala en Postman utilizando el botón Import en la sección superior izquierda.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/836f6199-9343-447a-9bce-23d8c07d0338" alt="Screenshot" width="800">

Una vez importada la colección, actualiza las variables de colección que especifican la URL donde se está ejecutando cada microservicio.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/efafbb3d-5938-4bd8-bfc7-6becfccd2682" alt="Screenshot" width="800">

Finalmente, ejecuta la colección haciendo clic derecho en su nombre y haciendo clic en el botón "Run collection", esto ejecutará múltiples solicitudes API y también ejecutará algunos assertions que hemos preparado para asegurarnos de que el microservicio esté funcionando como se espera.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/f5ca6f7c-e4f4-4209-a949-dcf3a6dab9e3" alt="Screenshot" width="800">

## Ejecutar evaluador github action workflow

Para las entregas 1 y 2, hemos proporcionado un evaluador automático que ejecutará validaciones en los servicios API expuestos en cada entrega. Este evaluador se ejecuta como un workflow de Github Actions en el repositorio. Para ejecutar el workflow, ve a la sección de "Actions" del repositorio que se encuentra en la parte superior.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/92d686b7-21b1-42b1-b23a-e8c3d626dfd3" alt="Screenshot" width="800">

Luego, encontrarás en la sección izquierda una lista de todos los flujos de trabajo (workflows) disponibles para ejecución. En este caso, verás "Evaluator_Entrega1" y "Evaluator_Entrega2", correspondientes a los evaluadores de las dos primeras entregas. Haz clic en el que deseas ejecutar. Verás un botón "Run workflow" en la sección superior derecha, haz clic en este botón, selecciona la rama en la que deseas ejecutarlo y haz clic en el botón "Run workflow".

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/4bcf1c0d-e422-4f9d-9ff6-a663f8248352" alt="Screenshot" width="800">

Esto iniciará la ejecución del workflow en la rama. Si todo funciona correctamente y la entrega es correcta, verás que todas las comprobaciones aparecen como aprobadas (passed).

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/proyecto-202314-base/assets/78829363/c6c580b2-80e0-411d-8971-a252312ce5ea" alt="Screenshot" width="800">

# Ejecución Entrega 2
El archivo ci_pipeline.yaml contiene la configuración para el proceso de Integración Continua (CI) de un proyecto; específicamente, define una serie de trabajos (Jobs) que se ejecutan automáticamente en eventos particulares, como el push de código a las ramas "main" y "develop". Uno de estos trabajos se llama test_entrega2.

El job test_entrega2 se encarga de todas las pruebas relacionadas con la segunda entrega del proyecto; aquí detallamos sus pasos específicos:

1.	Configuración del Entorno: Ejecutamos la tarea en una máquina virtual con el sistema operativo Ubuntu; en este caso, utilizamos la versión 3.9 de Python.

2.	Preparación del Entorno de Python: Configuramos la versión especificada de Python e instalamos todas las herramientas necesarias para el proyecto, garantizando así un funcionamiento sin problemas y procesos de desarrollo.

3.	Instalación de Dependencias: Nos dirigimos al directorio ./entrega2 e instalamos las dependencias del proyecto utilizando Pipenv, asegurando que todas las bibliotecas necesarias estén disponibles para las pruebas.

4.	Configuración de la Base de Datos: Instalamos una instancia de PostgreSQL en un contenedor Docker, específicamente para la Prueba de Entrega 2; establecemos las credenciales para asegurarnos de que la base de datos esté disponible antes de continuar.

5.	Ejecución de Pruebas Unitarias: Finalmente, se ejecutan las pruebas unitarias del proyecto utilizando Pytest, y posteriormente se configuran las variables de entorno como el nombre de la base de datos, el host y otras configuraciones relacionadas. Estas pruebas incluyen la medición de la cobertura del código; si la cobertura es inferior al 70%, se considera que el trabajo ha fallado.

<img src="https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202314-proyecto-grupo17/assets/56740710/351a89fd-1ecd-457d-8f54-885d10654137" alt="Screenshot" width="800">


En resumen, la función de test_entrega2 es automatizar la ejecución de las pruebas de entrega 2, asegurando que el entorno esté configurado de manera adecuada y consistente. Si la cobertura de código no alcanza un mínimo de 70%, esto indica un fallo en nuestro proceso de integración continua; estos parámetros garantizan pruebas rigurosas antes de implementar en las ramas principales del proyecto.


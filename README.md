# Taller Docker

API REST pequena construida con FastAPI que genera una cedula aleatoria.

## Requisitos

- Docker Desktop con Docker Compose habilitado.
- Puerto `8000` disponible en el equipo local.

## Levantar el servicio

Desde la raiz del proyecto, ejecuta:

```powershell
docker compose up --build
```

Para levantarlo en segundo plano:

```powershell
docker compose up --build -d
```

El servicio quedara disponible en:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Especificacion OpenAPI JSON: http://localhost:8000/openapi.json

## Endpoint

### Obtener una cedula

`GET /obtenerCedula`

No requiere parametros ni body de entrada. Cada llamada genera un numero aleatorio de 10 digitos.

Ejemplo con PowerShell:

```powershell
Invoke-RestMethod http://localhost:8000/obtenerCedula
```

Ejemplo con cURL:

```bash
curl http://localhost:8000/obtenerCedula
```

Respuesta `200 OK`:

```json
{
  "cedula": 1234567890
}
```

El valor de `cedula` cambia en cada solicitud.

## Coleccion de Postman

La coleccion lista para importar esta en [postman_collection.json](postman_collection.json).

1. Abre Postman.
2. Selecciona **Import**.
3. Elige `postman_collection.json`.
4. Ejecuta la solicitud **Obtener cedula**.

La variable `baseUrl` apunta por defecto a `http://localhost:8000`.

## Swagger / OpenAPI

FastAPI genera Swagger automaticamente a partir de la aplicacion. No es necesario instalar ni configurar un servidor adicional: abre [http://localhost:8000/docs](http://localhost:8000/docs) con el contenedor ejecutandose.

Tambien se incluye una especificacion independiente en [openapi.yaml](openapi.yaml), util para importar el contrato en herramientas compatibles con OpenAPI.

## Despliegue continuo en Render

El workflow [deploy-render.yml](.github/workflows/deploy-render.yml) despliega automaticamente en Render cada vez que se hace push a la rama `main`. Tambien puede ejecutarse manualmente desde la pestana **Actions** de GitHub.

### 1. Crear el servicio gratuito en Render

1. Ingresa a [render.com](https://render.com) y crea una cuenta.
2. Selecciona **New > Web Service**.
3. Conecta el repositorio `Canartovi97/taller-docker`.
4. Selecciona la rama `main`.
5. Elige **Docker** como entorno.
6. Usa `DockerFile` como ruta del Dockerfile si Render solicita especificarla.
7. Selecciona la instancia gratuita (**Free**).
8. Crea el servicio.

Render asignara una URL publica similar a `https://taller-docker.onrender.com`.

### 2. Crear el Deploy Hook

En el servicio de Render, abre **Settings > Deploy Hook**, crea un hook y copia su URL. La URL es secreta y no debe escribirse en el repositorio.

### 3. Guardar el secreto en GitHub

En GitHub abre el repositorio y ve a **Settings > Secrets and variables > Actions > New repository secret**:

- **Name:** `RENDER_DEPLOY_HOOK_URL`
- **Secret:** pega la URL del Deploy Hook de Render

### 4. Probar el despliegue

Haz un commit y push a `main`:

```powershell
git add .
git commit -m "deploy: configure continuous deployment"
git push origin main
```

GitHub ejecutara el workflow y Render iniciara el despliegue. El resultado se puede consultar en **GitHub > Actions** y en los logs del servicio de Render.

Cuando el servicio este activo, prueba:

```powershell
Invoke-RestMethod https://TU-SERVICIO.onrender.com/obtenerCedula
```

Swagger quedara disponible en `https://TU-SERVICIO.onrender.com/docs`.

> En el plan gratuito, Render puede suspender el servicio despues de un periodo de inactividad. La primera solicitud posterior puede tardar unos segundos mientras el servicio vuelve a activarse.

## Detener y administrar el contenedor

Detener y eliminar el contenedor:

```powershell
docker compose down
```

Ver logs:

```powershell
docker compose logs -f api
```

Ver el estado de los servicios:

```powershell
docker compose ps
```

## Ejecucion local sin Docker

Opcionalmente, con Python instalado:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Luego visita http://localhost:8000/docs.

## Solucion de problemas

- Si el puerto `8000` esta ocupado, cambia `"8000:8000"` en `docker-compose.yml` por otro puerto, por ejemplo `"8080:8000"`, y usa `http://localhost:8080`.
- Si modificas `requirements.txt` o `DockerFile`, vuelve a construir con `docker compose up --build`.

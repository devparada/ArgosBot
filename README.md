# ArgosBot

ArgosBot es un bot de monitorización *serverless* diseñado para vigilar la infraestructura de red del hogar (luz e internet) y notificar caídas de forma instantánea.

## Características

* **Monitoreo Externo (Cron)**: Disparado mediante un **Cloudflare Worker** independiente, superando las limitaciones de los planes gratuitos de Vercel Cron.
* **Notificaciones de Estado**: Alerta al detectar una transición de estado (Online a Offline) y confirma la recuperación calculando el tiempo total de inactividad (*downtime*).
* **Costo Cero**: Arquitectura basada en la *cuota gratuita* de Vercel, Upstash Redis y Cloudflare Workers.
* **Interfaz de Control**: Comandos interactivos a través del chat de Telegram (como `/status` y `/hello`) para comprobar el estado bajo demanda.

## Tecnologías Usadas

* **[FastAPI](https://fastapi.tiangolo.com/)**: Framework asíncrono para la API en Vercel.
* **[Vercel](https://vercel.com/)**: Alojamiento *serverless* del backend.
* **[Upstash Redis](https://upstash.com/)**: Persistencia de estados mediante REST API.
* **[Cloudflare Workers](https://workers.cloudflare.com/)**: Motor de ejecución del Cron externo (Nota: El script del worker no se incluye en este repositorio).
* **[Telegram Bot API](https://core.telegram.org/bots/api)**: Capa de interacción con el usuario.

## Dependencias (Python)

Las dependencias principales utilizadas en el proyecto (puedes ver la lista completa en el archivo `requirements.txt`) son:

* `fastapi`: Para construir la API de manera rápida y eficiente.
* `pydantic`: Para la validación de datos (usado internamente por FastAPI).
* `python-dotenv`: Para cargar las variables de entorno desde el archivo `.env` en desarrollo.
* `upstash-redis`: Cliente oficial de Upstash para conectar con Redis a través de peticiones HTTP/REST (ideal para entornos serverless).
* `httpx` y `requests`: Para realizar las peticiones HTTP al servidor monitorizado (TARGET_URL) y a la API de Telegram.

## Configuración y Despliegue

### 1. Variables de Entorno (`.env`)

Crea un archivo `.env` en la raíz copiando la plantilla proporcionada en `.env.example`. Asegúrate de rellenar los valores correctos:

```bash
cp .env.example .env
```

> [!CAUTION]
> La variable `TARGET_URL` **nunca** debe incluir el protocolo (`http://` o `https://`), ya que se concatena directamente en la lógica.

### 2. Despliegue del Backend en Vercel

1. Importa el repositorio en Vercel.
2. Configura todas las variables de entorno especificadas en el archivo `.env` en tu panel de Vercel.
3. El archivo `vercel.json` enrutará el tráfico automáticamente hacia `api/main.py`.

### 3. Configuración del Webhook

Ejecuta el siguiente comando para registrar el webhook en Telegram:

```bash
curl -F "url=https://tu-dominio-en-vercel.vercel.app/webhook/telegram" \
     -F "secret_token=EL_MISMO_SECRET_TOKEN_DEL_ENV" \
     "https://api.telegram.org/botTU_TELEGRAM_TOKEN/setWebhook"
```

### 4. Trigger Externo (Cloudflare Worker)

> [!IMPORTANT]
> El código fuente del Cloudflare Worker no está incluido en este repositorio.

Deberás crear y desplegar tu propio script en Cloudflare Workers configurándolo con un disparador cron (ej. cada 5 minutos) apuntando al endpoint `/api/cron_watchdog` de tu despliegue en Vercel, enviando la cabecera `X-Vercel-Cron: 1` para la autorización.

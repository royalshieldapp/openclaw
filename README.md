# openclaw

Backend en **FastAPI** para Royal Shield y un servicio separado de **OpenClaw Gateway** para Railway.

## FastAPI API

### Endpoints
- `GET /` estado general.
- `GET /health` healthcheck.
- `GET /ai?msg=...` consulta al modelo configurado en NVIDIA API Catalog.

### Variables
- `NVIDIA_API_KEY` (obligatoria para `/ai`).
- `AI_MODEL` (default: `meta/llama-3.1-8b-instruct`).
- `AI_PREMIUM_MODEL` (default: `meta/llama-3.3-70b-instruct`).
- `ENABLE_PREMIUM_MODEL` (default: `false`).
- `MAX_OUTPUT_TOKENS` (default: `2048`).
- `TEMPERATURE` (default: `0.7`).
- `PORT` (Railway la puede definir; fallback `8080`).

## OpenClaw Gateway + WhatsApp

El directorio `gateway/` se despliega como un **segundo servicio** en Railway, usando `/gateway` como Root Directory y un volumen persistente montado en `/data`.

### Modelos IA

El gateway usa Alibaba Cloud Model Studio mediante su API compatible con OpenAI y conserva NVIDIA como proveedor de respaldo:

- Primario: `qwen38/qwen3.8-27b`.
- Fallback: `nvidia/meta/llama-3.1-8b-instruct`.

### Railway

Configura el servicio `gateway` así:

1. **Root Directory:** `/gateway`
2. **Volume:** montar en `/data`
3. **Public Networking:** HTTP Proxy al puerto `8080`
4. **Variables secretas:**
   - `QWEN_API_KEY`
   - `NVIDIA_API_KEY`
   - `OPENCLAW_GATEWAY_TOKEN`
5. Railway debe exponer `RAILWAY_PUBLIC_DOMAIN` después de habilitar un dominio público.
6. Variables recomendadas:
   - `OPENCLAW_GATEWAY_PORT=8080`
   - `OPENCLAW_STATE_DIR=/data/openclaw`
   - `OPENCLAW_CONFIG_PATH=/data/openclaw/openclaw.json`
   - `OPENCLAW_WORKSPACE_DIR=/data/openclaw/workspace`
   - `OPENCLAW_SYNC_CONFIG=true`

`OPENCLAW_SYNC_CONFIG=true` hace que la configuración versionada en el repo sea la fuente de verdad en cada reinicio. Antes de reemplazar una configuración persistida, `start.sh` guarda una copia como `openclaw.json.previous`. Si quieres conservar cambios hechos manualmente desde la UI entre redeploys, cambia esta variable a `false`.

### Control UI

Cuando el dominio esté activo, abre:

`https://<RAILWAY_PUBLIC_DOMAIN>/`

La UI usa autenticación por token y limita el origen del navegador al dominio público de Railway. No uses `allowedOrigins=["*"]` en producción.

### WhatsApp

WhatsApp usa el plugin oficial y queda con:

- DMs desconocidos: `pairing`.
- Grupos: `disabled`.
- Audio entrante: desactivado por ahora.

Para vincular la cuenta, abre una Shell del servicio en Railway y ejecuta:

```bash
openclaw channels login --channel whatsapp
```

Escanea el QR desde **WhatsApp > Settings > Linked Devices > Link a Device**.

### Verificación

Desde Railway Shell:

```bash
openclaw doctor --json
openclaw gateway health --port "${PORT:-8080}"
```

El healthcheck del servicio usa `GET /healthz`.

## Desarrollo local de FastAPI

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Seguridad

No guardes en GitHub `QWEN_API_KEY`, `NVIDIA_API_KEY`, `OPENCLAW_GATEWAY_TOKEN`, credenciales de WhatsApp ni números permitidos. Los secretos deben vivir únicamente en Railway Variables y las credenciales/estado persistente en el volumen `/data`.

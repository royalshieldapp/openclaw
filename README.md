# openclaw

Backend en **FastAPI** para Royal Shield y un Gateway oficial de OpenClaw separado, listo para desplegar en Railway.

## Backend FastAPI (raiz)

### Endpoints
- `GET /` estado general.
- `GET /health` healthcheck para Railway.
- `GET /ai?msg=...` consulta al modelo configurado en NVIDIA API Catalog.

### Variables de entorno del backend

#### Requeridas
- `NVIDIA_API_KEY` (obligatoria para `/ai`).

#### Configuracion de modelos IA
- `AI_MODEL` (default: `meta/llama-3.1-8b-instruct`) - Modelo estandar para consultas normales.
- `AI_PREMIUM_MODEL` (default: `meta/llama-3.3-70b-instruct`) - Modelo premium (solo si `ENABLE_PREMIUM_MODEL=true`).
- `ENABLE_PREMIUM_MODEL` (default: `false`).
- `MAX_OUTPUT_TOKENS` (default: `2048`).
- `TEMPERATURE` (default: `0.7`).

#### Opcionales
- `PORT` (la define Railway automaticamente, default: `8080`).

### Deploy del backend en Railway
1. Conecta este repo en Railway.
2. En **Variables**, agrega `NVIDIA_API_KEY` y las variables de modelo que quieras sobrescribir.
3. Railway detectara `railway.toml` y ejecutara `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`.
4. El healthcheck usa `GET /health`.

## Gateway OpenClaw + WhatsApp

El directorio `gateway/` contiene un Gateway oficial de OpenClaw separado para vincular WhatsApp Web mediante QR. En Railway debe desplegarse como otro servicio con `/gateway` como directorio raiz y un volumen persistente montado en `/data`.

### Arquitectura de modelos

- **Primary:** `qwen38/qwen3.8-27b`
- **Provider:** Alibaba Cloud Model Studio, usando su API OpenAI-compatible.
- **Fallback:** `nvidia/meta/llama-3.1-8b-instruct`

La configuracion del repo se copia al `OPENCLAW_CONFIG_PATH` en cada arranque para evitar que un archivo persistente antiguo mantenga un modelo primario obsoleto. El workspace y las sesiones persistentes permanecen bajo `OPENCLAW_STATE_DIR`.

### Variables requeridas en el servicio `/gateway`

- `QWEN_API_KEY` - API key de Alibaba Cloud Model Studio para Qwen.
- `NVIDIA_API_KEY` - API key existente de NVIDIA para el fallback.
- `OPENCLAW_GATEWAY_TOKEN` - token de autenticacion del Gateway.

### Variables de estado

- `OPENCLAW_STATE_DIR=/data/openclaw`
- `OPENCLAW_CONFIG_PATH=/data/openclaw/openclaw.json`
- `OPENCLAW_WORKSPACE_DIR=/data/openclaw/workspace`

Railway suministra `PORT` automaticamente. El Gateway usa `/healthz` como healthcheck.

### Seguridad del canal

- Los mensajes directos usan emparejamiento.
- Los grupos permanecen desactivados.
- No se guardan API keys ni tokens en el repositorio.
- El audio entrante permanece desactivado hasta integrar y verificar un adaptador compatible.

## Desarrollo local del backend FastAPI

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Tests

```bash
python -m pytest
```

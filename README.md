# openclaw

Backend en **FastAPI** para OpenClaw, listo para desplegar en Railway.

## Endpoints
- `GET /` estado general.
- `GET /health` healthcheck para Railway.
- `GET /ai?msg=...` consulta al modelo configurado en NVIDIA API Catalog.

## Variables de entorno

### Requeridas
- `NVIDIA_API_KEY` (obligatoria para `/ai`).

### Configuración de modelos IA
- `AI_MODEL` (default: `meta/llama-3.1-8b-instruct`) - Modelo estándar para consultas normales.
- `AI_PREMIUM_MODEL` (default: `meta/llama-3.3-70b-instruct`) - Modelo premium (solo si `ENABLE_PREMIUM_MODEL=true`).
- `ENABLE_PREMIUM_MODEL` (default: `false`) - Activar modelos premium (caro).
- `MAX_OUTPUT_TOKENS` (default: `2048`) - Tokens máximos de salida.
- `TEMPERATURE` (default: `0.7`) - Temperatura del modelo (0.0 - 1.0).

### Opcionales
- `PORT` (la define Railway automáticamente, default: `8080`).

## Deploy en Railway
1. Conecta este repo en Railway.
2. En **Variables**, agrega:
   - `NVIDIA_API_KEY` (tu clave de NVIDIA API Catalog)
   - `AI_MODEL=meta/llama-3.1-8b-instruct`
   - `ENABLE_PREMIUM_MODEL=false` (solo cambia a true si es necesario)
3. Railway detectará `railway.toml` y ejecutará:
   - `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
4. El healthcheck usa `GET /health`.

## Desarrollo local
```bash
# Configura NVIDIA_API_KEY en tu entorno
pip install -r requirements.txt
uvicorn main:app --reload
```

## Modelos disponibles
- **meta/llama-3.1-8b-instruct** - Default
- **meta/llama-3.3-70b-instruct** - Solo si `ENABLE_PREMIUM_MODEL=true`

La disponibilidad de modelos depende del catálogo activo de NVIDIA.

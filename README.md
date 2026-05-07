# openclaw

Backend en **FastAPI** para OpenClaw, listo para desplegar en Railway.

## Endpoints
- `GET /` estado general.
- `GET /health` healthcheck para Railway.
- `GET /ai?msg=...` consulta al modelo de OpenAI.

## Variables de entorno

### Requeridas
- `OPENAI_API_KEY` (obligatoria para `/ai`).

### Configuración de modelos IA
- `AI_MODEL` (default: `gpt-4o-mini`) - Modelo estándar para consultas normales.
- `AI_FALLBACK_MODEL` (default: `gpt-4o-mini`) - Modelo de respaldo.
- `AI_PREMIUM_MODEL` (default: `gpt-4-turbo`) - Modelo premium de alta calidad (solo si `ENABLE_PREMIUM_MODEL=true`).
- `ENABLE_PREMIUM_MODEL` (default: `false`) - Activar modelos premium (caro).
- `MAX_OUTPUT_TOKENS` (default: `2048`) - Tokens máximos de salida.
- `TEMPERATURE` (default: `0.7`) - Temperatura del modelo (0.0 - 1.0).

### Opcionales
- `PORT` (la define Railway automáticamente, default: `8080`).

## Deploy en Railway
1. Conecta este repo en Railway.
2. En **Variables**, agrega:
   - `OPENAI_API_KEY` (tu clave de API de OpenAI)
   - `AI_MODEL=gpt-4o-mini` (recomendado para costos bajos)
   - `ENABLE_PREMIUM_MODEL=false` (solo cambia a true si es necesario)
3. Railway detectará `railway.toml` y ejecutará:
   - `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
4. El healthcheck usa `GET /health`.

## Desarrollo local
```bash
cp .env.example .env
# Edita .env con tu OPENAI_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload
```

## Modelos disponibles
- **gpt-4o-mini** (recomendado, bajo costo) - Default
- **gpt-4o** (costo medio, mejor calidad)
- **gpt-4-turbo** (costo alto, máxima calidad) - Solo si `ENABLE_PREMIUM_MODEL=true`

**Nota**: Claude Opus ha sido removido. Usa gpt-4o-mini por defecto para optimizar costos.

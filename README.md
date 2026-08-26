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
- `AI_MODEL` (default: `qwen/qwen3.8-27b`) - Modelo estándar para consultas normales con Qwen 3.8.
- `AI_PREMIUM_MODEL` (default: `qwen/qwen3.8-max`) - Modelo premium Qwen 3.8 Max (solo si `ENABLE_PREMIUM_MODEL=true`).
- `ENABLE_PREMIUM_MODEL` (default: `false`) - Activar modelos premium (más potente y costoso).
- `MAX_OUTPUT_TOKENS` (default: `2048`) - Tokens máximos de salida.
- `TEMPERATURE` (default: `0.7`) - Temperatura del modelo (0.0 - 1.0).

### Opcionales
- `PORT` (la define Railway automáticamente, default: `8080`).

## Deploy en Railway
1. Conecta este repo en Railway.
2. En **Variables**, agrega:
   - `NVIDIA_API_KEY` (tu clave de NVIDIA API Catalog)
   - `AI_MODEL=qwen/qwen3.8-27b` (Qwen 3.8 27B)
   - `ENABLE_PREMIUM_MODEL=false` (solo cambia a true si necesitas Qwen 3.8 Max)
3. Railway detectará `railway.toml` y ejecutará:
   - `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
4. El healthcheck usa `GET /health`.

## Desarrollo local
```bash
# Configura NVIDIA_API_KEY en tu entorno
pip install -r requirements.txt
uvicorn main:app --reload
```

## Gateway separado de WhatsApp

El directorio `gateway/` contiene un Gateway oficial de OpenClaw separado para
vincular WhatsApp Web mediante QR. En Railway debe desplegarse como otro
servicio, con `/gateway` como directorio raíz y un volumen persistente montado
en `/data`.

Variables requeridas en ese servicio:

- `NVIDIA_API_KEY`
- `OPENCLAW_GATEWAY_TOKEN`

El canal usa emparejamiento para mensajes directos, bloquea grupos y no guarda
números ni secretos en el repositorio. El audio entrante permanece desactivado
hasta integrar y verificar un adaptador de voz compatible con NVIDIA.

## Modelos disponibles (QWEEN 3.8)
- **qwen/qwen3.8-27b** - Modelo denso de 27B, default y más eficiente
- **qwen/qwen3.8-max** - Modelo MoE de máxima capacidad (2.4T parámetros), solo con `ENABLE_PREMIUM_MODEL=true`

La disponibilidad de modelos depende del catálogo activo de NVIDIA.

## Actualizaciones Qwen 3.8
- Mejoras sustanciales en programación, trabajo profesional e investigación
- Mejor control de tareas complejas y multi-paso
- Compatibilidad extendida con frameworks y herramientas


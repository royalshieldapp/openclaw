# openclaw

Backend en **FastAPI** para OpenClaw, listo para desplegar en Railway.

## Endpoints
- `GET /` estado general.
- `GET /health` healthcheck para Railway.
- `GET /ai?msg=...` consulta al modelo de OpenAI.

## Variables de entorno
- `OPENAI_API_KEY` (obligatoria para `/ai`).
- `PORT` (la define Railway automáticamente).

## Deploy en Railway
1. Conecta este repo en Railway.
2. En **Variables**, agrega `OPENAI_API_KEY`.
3. Railway detectará `railway.toml` y ejecutará:
   - `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}`
4. El healthcheck usa `GET /health`.

## Desarrollo local
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

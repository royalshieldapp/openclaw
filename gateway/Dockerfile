FROM node:24.17.0-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates ffmpeg tini \
    && rm -rf /var/lib/apt/lists/* \
    && npm install --global \
        openclaw@2026.7.1-2 \
        @openclaw/whatsapp@2026.7.1

WORKDIR /app

COPY openclaw.json /app/openclaw.json
COPY start.sh /app/start.sh

RUN chmod 0555 /app/start.sh \
    && mkdir -p /data/openclaw \
    && chown -R node:node /data

ENV OPENCLAW_STATE_DIR=/data/openclaw \
    OPENCLAW_CONFIG_PATH=/data/openclaw/openclaw.json \
    OPENCLAW_WORKSPACE_DIR=/data/openclaw/workspace \
    OPENCLAW_DISABLE_BONJOUR=1 \
    NODE_ENV=production

EXPOSE 18789

USER node

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/app/start.sh"]

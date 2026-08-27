#!/bin/sh
set -eu

require_env() {
    name="$1"
    eval "value=\${$name:-}"
    if [ -z "$value" ]; then
        echo "Required environment variable is missing: $name" >&2
        exit 1
    fi
}

require_env "NVIDIA_API_KEY"
require_env "OPENCLAW_GATEWAY_TOKEN"
require_env "RAILWAY_PUBLIC_DOMAIN"

: "${OPENCLAW_STATE_DIR:=/data/openclaw}"
: "${OPENCLAW_CONFIG_PATH:=${OPENCLAW_STATE_DIR}/openclaw.json}"
: "${OPENCLAW_WORKSPACE_DIR:=${OPENCLAW_STATE_DIR}/workspace}"
: "${OPENCLAW_SYNC_CONFIG:=true}"
OPENCLAW_GATEWAY_PORT="${PORT:-${OPENCLAW_GATEWAY_PORT:-8080}}"

export OPENCLAW_STATE_DIR
export OPENCLAW_CONFIG_PATH
export OPENCLAW_WORKSPACE_DIR
export OPENCLAW_GATEWAY_PORT

mkdir -p "$OPENCLAW_STATE_DIR" "$OPENCLAW_WORKSPACE_DIR"

if [ ! -f "$OPENCLAW_CONFIG_PATH" ] || [ "$OPENCLAW_SYNC_CONFIG" = "true" ]; then
    if [ -f "$OPENCLAW_CONFIG_PATH" ]; then
        cp "$OPENCLAW_CONFIG_PATH" "${OPENCLAW_CONFIG_PATH}.previous"
    fi
    cp /app/openclaw.json "$OPENCLAW_CONFIG_PATH"
fi

exec openclaw gateway --bind lan --port "$OPENCLAW_GATEWAY_PORT"

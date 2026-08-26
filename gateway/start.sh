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

require_env "QWEN_API_KEY"
require_env "NVIDIA_API_KEY"
require_env "OPENCLAW_GATEWAY_TOKEN"

: "${OPENCLAW_STATE_DIR:=/data/openclaw}"
: "${OPENCLAW_CONFIG_PATH:=${OPENCLAW_STATE_DIR}/openclaw.json}"
: "${OPENCLAW_WORKSPACE_DIR:=${OPENCLAW_STATE_DIR}/workspace}"
OPENCLAW_GATEWAY_PORT="${PORT:-${OPENCLAW_GATEWAY_PORT:-18789}}"

export OPENCLAW_STATE_DIR
export OPENCLAW_CONFIG_PATH
export OPENCLAW_WORKSPACE_DIR
export OPENCLAW_GATEWAY_PORT

mkdir -p "$OPENCLAW_STATE_DIR" "$OPENCLAW_WORKSPACE_DIR"

# Keep the versioned gateway configuration authoritative on each deploy while
# preserving workspace/channel session state under OPENCLAW_STATE_DIR.
cp /app/openclaw.json "$OPENCLAW_CONFIG_PATH"
chmod 0600 "$OPENCLAW_CONFIG_PATH"

exec openclaw gateway --bind lan --port "$OPENCLAW_GATEWAY_PORT"

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "gateway"


def test_gateway_container_uses_pinned_openclaw_versions():
    dockerfile = (GATEWAY / "Dockerfile").read_text(encoding="utf-8")

    assert "openclaw@2026.7.1-2" in dockerfile
    assert "@openclaw/whatsapp@2026.7.1" in dockerfile
    assert "USER node" in dockerfile


def test_gateway_config_is_secure_and_uses_qwen_primary_with_nvidia_fallback():
    config = (GATEWAY / "openclaw.json").read_text(encoding="utf-8")

    assert '"primary": "qwen38/qwen3.8-27b"' in config
    assert '"nvidia/meta/llama-3.1-8b-instruct"' in config
    assert '"baseUrl": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"' in config
    assert '"apiKey": "${QWEN_API_KEY}"' in config
    assert '"api": "openai-completions"' in config
    assert '"supportsTools": true' in config
    assert '"dmPolicy": "pairing"' in config
    assert '"groupPolicy": "disabled"' in config
    assert "${OPENCLAW_GATEWAY_TOKEN}" in config
    assert "qwen/qwen3.5-397b-a17b" not in config
    assert "nvapi-" not in config
    assert "sk-" not in config
    assert "+1555" not in config


def test_gateway_startup_requires_secrets_and_syncs_repo_config():
    startup = (GATEWAY / "start.sh").read_text(encoding="utf-8")
    dockerfile = (GATEWAY / "Dockerfile").read_text(encoding="utf-8")

    assert 'require_env "QWEN_API_KEY"' in startup
    assert 'require_env "NVIDIA_API_KEY"' in startup
    assert 'require_env "OPENCLAW_GATEWAY_TOKEN"' in startup
    assert 'require_env "RAILWAY_PUBLIC_DOMAIN"' in startup
    assert "OPENCLAW_STATE_DIR:=/data/openclaw" in startup
    assert 'OPENCLAW_GATEWAY_PORT="${PORT:-${OPENCLAW_GATEWAY_PORT:-8080}}"' in startup
    assert "OPENCLAW_GATEWAY_PORT=18789" not in dockerfile
    assert 'OPENCLAW_SYNC_CONFIG:=true' in startup
    assert '${OPENCLAW_CONFIG_PATH}.previous' in startup
    assert "cp /app/openclaw.json" in startup
    assert 'chmod 0600 "$OPENCLAW_CONFIG_PATH"' in startup
    assert "exec openclaw gateway" in startup


def test_gateway_env_example_documents_railway_runtime():
    env_example = (GATEWAY / ".env.example").read_text(encoding="utf-8")

    assert "RAILWAY_PUBLIC_DOMAIN=" in env_example
    assert "OPENCLAW_GATEWAY_PORT=8080" in env_example
    assert "OPENCLAW_SYNC_CONFIG=true" in env_example
    assert "nvapi-" not in env_example


def test_railway_gateway_configuration_targets_healthcheck():
    railway = (GATEWAY / "railway.toml").read_text(encoding="utf-8")

    assert 'dockerfilePath = "Dockerfile"' in railway
    assert 'healthcheckPath = "/healthz"' in railway
    assert 'startCommand = "/app/start.sh"' in railway

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GATEWAY = ROOT / "gateway"


def test_gateway_container_uses_pinned_openclaw_versions():
    dockerfile = (GATEWAY / "Dockerfile").read_text(encoding="utf-8")

    assert "openclaw@2026.7.1-2" in dockerfile
    assert "@openclaw/whatsapp@2026.7.1" in dockerfile
    assert "USER node" in dockerfile


def test_gateway_config_is_secure_and_uses_nvidia():
    config = (GATEWAY / "openclaw.json").read_text(encoding="utf-8")

    assert '"primary": "nvidia/meta/llama-3.1-8b-instruct"' in config
    assert '"dmPolicy": "pairing"' in config
    assert '"groupPolicy": "disabled"' in config
    assert "${OPENCLAW_GATEWAY_TOKEN}" in config
    assert "nvapi-" not in config
    assert "+1555" not in config


def test_gateway_startup_requires_secrets_and_persistent_state():
    startup = (GATEWAY / "start.sh").read_text(encoding="utf-8")

    assert 'require_env "NVIDIA_API_KEY"' in startup
    assert 'require_env "OPENCLAW_GATEWAY_TOKEN"' in startup
    assert "OPENCLAW_STATE_DIR:=/data/openclaw" in startup
    assert "exec openclaw gateway" in startup


def test_railway_gateway_configuration_targets_healthcheck():
    railway = (GATEWAY / "railway.toml").read_text(encoding="utf-8")

    assert 'dockerfilePath = "Dockerfile"' in railway
    assert 'healthcheckPath = "/healthz"' in railway
    assert 'startCommand = "/app/start.sh"' in railway

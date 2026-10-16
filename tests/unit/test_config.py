"""Unit tests for runtime config loaded from env vars."""

from student_system.config import load_config


def test_config_defaults(monkeypatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("PAYMENT_MODE", raising=False)
    monkeypatch.delenv("DEFAULT_GROUP", raising=False)
    config = load_config()
    assert config.environment == "development"
    assert config.payment_mode == "sandbox"
    assert config.default_group == "PI-21"


def test_config_from_env(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("PAYMENT_MODE", "live")
    monkeypatch.setenv("DEFAULT_GROUP", "PI-99")
    config = load_config()
    assert config.environment == "testing"
    assert config.payment_mode == "live"
    assert config.default_group == "PI-99"


def test_config_partial_env(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")
    monkeypatch.delenv("PAYMENT_MODE", raising=False)
    monkeypatch.delenv("DEFAULT_GROUP", raising=False)
    config = load_config()
    assert config.environment == "staging"
    assert config.payment_mode == "sandbox"
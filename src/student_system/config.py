"""Runtime configuration from environment variables."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    environment: str
    payment_mode: str
    default_group: str


def load_config() -> RuntimeConfig:
    """Load config from env vars with defaults."""
    return RuntimeConfig(
        environment=os.getenv("APP_ENV", "development"),
        payment_mode=os.getenv("PAYMENT_MODE", "sandbox"),
        default_group=os.getenv("DEFAULT_GROUP", "PI-21"),
    )
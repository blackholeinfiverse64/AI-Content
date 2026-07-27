"""
Integration Configuration
Loads and validates all ecosystem service configurations from environment variables.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# --- Ecosystem Service URLs ---
BHIV_CORE_URL = os.getenv("BHIV_CORE_URL", "")
CREATOR_CORE_URL = os.getenv("CREATOR_CORE_URL", "")
PROMPT_RUNNER_URL = os.getenv("PROMPT_RUNNER_URL", "")
BUCKET_SERVICE_URL = os.getenv("BUCKET_SERVICE_URL", "")
INSIGHTFLOW_URL = os.getenv("INSIGHTFLOW_URL", "")
TANTRA_URL = os.getenv("TANTRA_URL", "")

# --- API Keys ---
BHIV_CORE_API_KEY = os.getenv("BHIV_CORE_API_KEY", "")
CREATOR_CORE_API_KEY = os.getenv("CREATOR_CORE_API_KEY", "")
PROMPT_RUNNER_API_KEY = os.getenv("PROMPT_RUNNER_API_KEY", "")
BUCKET_SERVICE_API_KEY = os.getenv("BUCKET_SERVICE_API_KEY", "")
INSIGHTFLOW_API_KEY = os.getenv("INSIGHTFLOW_API_KEY", "")

# --- Timeouts ---
BHIV_CORE_TIMEOUT = int(os.getenv("BHIV_CORE_TIMEOUT", "30"))
CREATOR_CORE_TIMEOUT = int(os.getenv("CREATOR_CORE_TIMEOUT", "30"))
PROMPT_RUNNER_TIMEOUT = int(os.getenv("PROMPT_RUNNER_TIMEOUT", "60"))
BUCKET_SERVICE_TIMEOUT = int(os.getenv("BUCKET_SERVICE_TIMEOUT", "30"))
INSIGHTFLOW_TIMEOUT = int(os.getenv("INSIGHTFLOW_TIMEOUT", "10"))
TANTRA_TIMEOUT = int(os.getenv("TANTRA_TIMEOUT", "15"))

# --- Platform Identity ---
PLATFORM_ID = os.getenv("PLATFORM_ID", "ai_content_platform")
PLATFORM_SCHEMA_VERSION = os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def get_integration_config() -> Dict[str, Any]:
    """Return full integration configuration (excluding secrets)."""
    return {
        "platform_id": PLATFORM_ID,
        "schema_version": PLATFORM_SCHEMA_VERSION,
        "environment": ENVIRONMENT,
        "services": {
            "bhiv_core": {
                "url": BHIV_CORE_URL or "not_configured",
                "configured": bool(BHIV_CORE_URL),
                "timeout": BHIV_CORE_TIMEOUT,
            },
            "creator_core": {
                "url": CREATOR_CORE_URL or "not_configured",
                "configured": bool(CREATOR_CORE_URL),
                "timeout": CREATOR_CORE_TIMEOUT,
            },
            "prompt_runner": {
                "url": PROMPT_RUNNER_URL or "not_configured",
                "configured": bool(PROMPT_RUNNER_URL),
                "timeout": PROMPT_RUNNER_TIMEOUT,
            },
            "bucket": {
                "url": BUCKET_SERVICE_URL or "not_configured",
                "configured": bool(BUCKET_SERVICE_URL),
                "timeout": BUCKET_SERVICE_TIMEOUT,
            },
            "insightflow": {
                "url": INSIGHTFLOW_URL or "not_configured",
                "configured": bool(INSIGHTFLOW_URL),
                "timeout": INSIGHTFLOW_TIMEOUT,
            },
            "tantra": {
                "url": TANTRA_URL or "not_configured",
                "configured": bool(TANTRA_URL),
                "timeout": TANTRA_TIMEOUT,
            },
        },
    }


def get_configured_services() -> list:
    """Return list of configured external services."""
    services = []
    if BHIV_CORE_URL:
        services.append("bhiv_core")
    if CREATOR_CORE_URL:
        services.append("creator_core")
    if PROMPT_RUNNER_URL:
        services.append("prompt_runner")
    if BUCKET_SERVICE_URL:
        services.append("bucket")
    if INSIGHTFLOW_URL:
        services.append("insightflow")
    if TANTRA_URL:
        services.append("tantra")
    return services


def validate_integration_config() -> Dict[str, Any]:
    """Validate integration configuration and return status."""
    configured = get_configured_services()
    all_services = ["bhiv_core", "creator_core", "prompt_runner", "bucket", "insightflow", "tantra"]
    missing = [s for s in all_services if s not in configured]

    return {
        "valid": True,
        "configured_services": configured,
        "missing_services": missing,
        "total_configured": len(configured),
        "total_missing": len(missing),
        "platform_id": PLATFORM_ID,
        "schema_version": PLATFORM_SCHEMA_VERSION,
        "environment": ENVIRONMENT,
    }

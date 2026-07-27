"""
BHIV Ecosystem Integration Adapters
Each adapter connects to an external service with graceful fallback to local implementation.
Environment variables configure service URLs; when unset, local fallback is used.
"""

import os
import time
import json
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logger.warning("httpx not available - integration adapters will use local fallbacks only")


# =============================================================================
# BHIV Core Adapter
# =============================================================================

class BHIVCoreAdapter:
    """
    Routes requests through the external BHIV Core service.
    Falls back to local implementation when service is unavailable.
    """

    def __init__(self):
        self.base_url = os.getenv("BHIV_CORE_URL", "").rstrip("/")
        self.timeout = int(os.getenv("BHIV_CORE_TIMEOUT", "30"))
        self.api_key = os.getenv("BHIV_CORE_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers=headers,
            )
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "BHIV_CORE_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def register(self, platform_id: str, metadata: Dict = None) -> Dict[str, Any]:
        if not self.is_available():
            return {"status": "local", "message": "Using local BHIV Core"}
        try:
            client = self._get_client()
            payload = {
                "platform_id": platform_id,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "metadata": metadata or {},
            }
            resp = await client.post(f"{self.base_url}/register", json=payload)
            return resp.json()
        except Exception as e:
            logger.warning("BHIV Core registration failed: %s", e)
            return {"status": "error", "error": str(e)}

    async def route_request(self, trace_id: str, module: str, action: str,
                            payload: Dict, execution_id: str = None) -> Dict[str, Any]:
        if not self.is_available():
            return {"status": "local", "message": "BHIV Core not available, using local routing"}
        try:
            client = self._get_client()
            body = {
                "trace_id": trace_id,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "module": module,
                "action": action,
                "payload": payload,
                "execution_id": execution_id or f"exec_{int(time.time()*1000)}",
            }
            resp = await client.post(f"{self.base_url}/route", json=body)
            return resp.json()
        except Exception as e:
            logger.warning("BHIV Core routing failed: %s", e)
            return {"status": "error", "error": str(e)}

    async def execute(self, trace_id: str, module: str, action: str,
                      payload: Dict, execution_id: str = None) -> Dict[str, Any]:
        if not self.is_available():
            return {"status": "local", "message": "BHIV Core not available, using local execution"}
        try:
            client = self._get_client()
            body = {
                "trace_id": trace_id,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "module": module,
                "action": action,
                "payload": payload,
                "execution_id": execution_id or f"exec_{int(time.time()*1000)}",
            }
            resp = await client.post(f"{self.base_url}/execute", json=body)
            return resp.json()
        except Exception as e:
            logger.warning("BHIV Core execution failed: %s", e)
            return {"status": "error", "error": str(e)}


# =============================================================================
# Creator Core Adapter
# =============================================================================

class CreatorCoreAdapter:
    """
    Consumes structured blueprints from Creator Core.
    Falls back to local storyboard generation when unavailable.
    """

    def __init__(self):
        self.base_url = os.getenv("CREATOR_CORE_URL", "").rstrip("/")
        self.timeout = int(os.getenv("CREATOR_CORE_TIMEOUT", "30"))
        self.api_key = os.getenv("CREATOR_CORE_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "CREATOR_CORE_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def generate_blueprint(self, script_text: str, content_id: str,
                                 trace_id: str = None, metadata: Dict = None) -> Dict[str, Any]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            body = {
                "script_text": script_text,
                "content_id": content_id,
                "trace_id": trace_id or f"trace_{int(time.time()*1000)}",
                "metadata": metadata or {},
            }
            resp = await client.post(f"{self.base_url}/generate-blueprint", json=body)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            logger.warning("Creator Core blueprint generation failed: %s", e)
            return None

    async def get_blueprint(self, blueprint_id: str) -> Dict[str, Any]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/blueprint/{blueprint_id}")
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            logger.warning("Creator Core blueprint retrieval failed: %s", e)
            return None


# =============================================================================
# Prompt Runner Adapter
# =============================================================================

class PromptRunnerAdapter:
    """
    Executes prompts through the canonical Prompt Runner service.
    Falls back to direct LLM API calls when unavailable.
    """

    def __init__(self):
        self.base_url = os.getenv("PROMPT_RUNNER_URL", "").rstrip("/")
        self.timeout = int(os.getenv("PROMPT_RUNNER_TIMEOUT", "60"))
        self.api_key = os.getenv("PROMPT_RUNNER_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "PROMPT_RUNNER_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def execute(self, prompt: str, trace_id: str = None,
                      timeout: int = None, metadata: Dict = None) -> Dict[str, Any]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            body = {
                "prompt": prompt,
                "trace_id": trace_id or f"trace_{int(time.time()*1000)}",
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "timeout": timeout or self.timeout,
                "metadata": metadata or {},
            }
            resp = await client.post(f"{self.base_url}/execute", json=body)
            if resp.status_code == 200:
                return resp.json()
            logger.warning("Prompt Runner returned status %d", resp.status_code)
            return None
        except Exception as e:
            logger.warning("Prompt Runner execution failed: %s", e)
            return None

    async def execute_deterministic(self, prompt: str, trace_id: str = None,
                                    metadata: Dict = None) -> Dict[str, Any]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            body = {
                "prompt": prompt,
                "trace_id": trace_id or f"trace_{int(time.time()*1000)}",
                "mode": "deterministic",
                "metadata": metadata or {},
            }
            resp = await client.post(f"{self.base_url}/execute-deterministic", json=body)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            logger.warning("Prompt Runner deterministic execution failed: %s", e)
            return None


# =============================================================================
# Bucket Adapter
# =============================================================================

class BucketAdapter:
    """
    Persists execution artifacts through the canonical Bucket service.
    Falls back to local bhiv_bucket when unavailable.
    """

    def __init__(self):
        self.base_url = os.getenv("BUCKET_SERVICE_URL", "").rstrip("/")
        self.timeout = int(os.getenv("BUCKET_SERVICE_TIMEOUT", "30"))
        self.api_key = os.getenv("BUCKET_SERVICE_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "BUCKET_SERVICE_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def persist(self, segment: str, filename: str, data: Any,
                      trace_id: str = None) -> Dict[str, Any]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            body = {
                "segment": segment,
                "filename": filename,
                "data": data,
                "trace_id": trace_id,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
            }
            resp = await client.post(f"{self.base_url}/persist", json=body)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            logger.warning("Bucket service persist failed: %s", e)
            return None

    async def retrieve(self, segment: str, filename: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/retrieve/{segment}/{filename}")
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            logger.warning("Bucket service retrieve failed: %s", e)
            return None

    async def list_files(self, segment: str) -> list:
        if not self.is_available():
            return []
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/list/{segment}")
            if resp.status_code == 200:
                return resp.json().get("files", [])
            return []
        except Exception as e:
            logger.warning("Bucket service list failed: %s", e)
            return []


# =============================================================================
# InsightFlow Adapter
# =============================================================================

class InsightFlowAdapter:
    """
    Emits runtime telemetry and events to InsightFlow.
    Always non-blocking; never fails the caller.
    """

    def __init__(self):
        self.base_url = os.getenv("INSIGHTFLOW_URL", "").rstrip("/")
        self.timeout = int(os.getenv("INSIGHTFLOW_TIMEOUT", "10"))
        self.api_key = os.getenv("INSIGHTFLOW_API_KEY", "")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            self._client = httpx.AsyncClient(timeout=self.timeout, headers=headers)
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "INSIGHTFLOW_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def emit(self, event_type: str, data: Dict[str, Any],
                   trace_id: str = None, user_id: str = None) -> bool:
        if not self.is_available():
            return False
        try:
            client = self._get_client()
            body = {
                "event_type": event_type,
                "data": data,
                "trace_id": trace_id,
                "user_id": user_id,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "ai_content_platform",
            }
            resp = await client.post(f"{self.base_url}/emit", json=body)
            return resp.status_code == 200
        except Exception as e:
            logger.debug("InsightFlow emit failed (non-critical): %s", e)
            return False

    async def emit_batch(self, events: list) -> bool:
        if not self.is_available() or not events:
            return False
        try:
            client = self._get_client()
            body = {
                "events": events,
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "source": "ai_content_platform",
            }
            resp = await client.post(f"{self.base_url}/emit-batch", json=body)
            return resp.status_code == 200
        except Exception as e:
            logger.debug("InsightFlow batch emit failed (non-critical): %s", e)
            return False


# =============================================================================
# TANTRA Adapter
# =============================================================================

class TANTRAAdapter:
    """
    Registers and participates in the TANTRA runtime.
    Falls back gracefully when TANTRA is unavailable.
    """

    def __init__(self):
        self.base_url = os.getenv("TANTRA_URL", "").rstrip("/")
        self.timeout = int(os.getenv("TANTRA_TIMEOUT", "15"))
        self.platform_id = os.getenv("PLATFORM_ID", "ai_content_platform")
        self._client = None

    def _get_client(self):
        if self._client is None and HTTPX_AVAILABLE:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    def is_available(self) -> bool:
        return bool(self.base_url) and HTTPX_AVAILABLE

    async def health_check(self) -> Dict[str, Any]:
        if not self.is_available():
            return {"available": False, "reason": "TANTRA_URL not configured"}
        try:
            client = self._get_client()
            resp = await client.get(f"{self.base_url}/health")
            return {"available": True, "status": resp.status_code, "data": resp.json()}
        except Exception as e:
            return {"available": False, "error": str(e)}

    async def register(self, platform_metadata: Dict = None) -> Dict[str, Any]:
        if not self.is_available():
            return {"status": "local", "message": "TANTRA not available, running standalone"}
        try:
            client = self._get_client()
            body = {
                "platform_id": self.platform_id,
                "platform_name": "AI Content Platform",
                "schema_version": os.getenv("PLATFORM_SCHEMA_VERSION", "1.0.0"),
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "capabilities": [
                    "content_upload",
                    "video_generation",
                    "storyboard_creation",
                    "feedback_learning",
                    "tag_recommendation",
                ],
                "metadata": platform_metadata or {},
            }
            resp = await client.post(f"{self.base_url}/register", json=body)
            if resp.status_code == 200:
                return resp.json()
            return {"status": "error", "status_code": resp.status_code}
        except Exception as e:
            logger.warning("TANTRA registration failed: %s", e)
            return {"status": "error", "error": str(e)}

    async def report_status(self, status: Dict) -> Dict[str, Any]:
        if not self.is_available():
            return {"status": "local"}
        try:
            client = self._get_client()
            body = {
                "platform_id": self.platform_id,
                "status": status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            resp = await client.post(f"{self.base_url}/status", json=body)
            return resp.json() if resp.status_code == 200 else {"status": "error"}
        except Exception as e:
            logger.debug("TANTRA status report failed: %s", e)
            return {"status": "error", "error": str(e)}


# =============================================================================
# Integration Manager
# =============================================================================

class IntegrationManager:
    """
    Central manager for all ecosystem integrations.
    Provides unified access to all adapters and health checks.
    """

    def __init__(self):
        self.bhiv_core = BHIVCoreAdapter()
        self.creator_core = CreatorCoreAdapter()
        self.prompt_runner = PromptRunnerAdapter()
        self.bucket = BucketAdapter()
        self.insightflow = InsightFlowAdapter()
        self.tantra = TANTRAAdapter()

    async def health_check_all(self) -> Dict[str, Any]:
        results = {}
        adapters = {
            "bhiv_core": self.bhiv_core,
            "creator_core": self.creator_core,
            "prompt_runner": self.prompt_runner,
            "bucket": self.bucket,
            "insightflow": self.insightflow,
            "tantra": self.tantra,
        }
        for name, adapter in adapters.items():
            try:
                results[name] = await adapter.health_check()
            except Exception as e:
                results[name] = {"available": False, "error": str(e)}
        return results

    def get_integration_status(self) -> Dict[str, Any]:
        return {
            "bhiv_core": {"available": self.bhiv_core.is_available(), "url": self.bhiv_core.base_url or "not_configured"},
            "creator_core": {"available": self.creator_core.is_available(), "url": self.creator_core.base_url or "not_configured"},
            "prompt_runner": {"available": self.prompt_runner.is_available(), "url": self.prompt_runner.base_url or "not_configured"},
            "bucket": {"available": self.bucket.is_available(), "url": self.bucket.base_url or "not_configured"},
            "insightflow": {"available": self.insightflow.is_available(), "url": self.insightflow.base_url or "not_configured"},
            "tantra": {"available": self.tantra.is_available(), "url": self.tantra.base_url or "not_configured"},
        }


# Global singleton
integration_manager = IntegrationManager()

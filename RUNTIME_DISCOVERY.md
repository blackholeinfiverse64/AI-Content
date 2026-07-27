# Runtime Discovery & Registration

## Overview
The AI Content Platform discovers and registers with the BHIV ecosystem at startup via canonical adapter clients. Registration is non-blocking — if any service is unavailable, the platform continues operating standalone.

## Startup Flow

```
Startup Event
├── Validate integration config (env vars)
├── Register with TANTRA Runtime (execution infrastructure)
├── Register with BHIV Core (intelligent processing pipeline)
├── Emit startup event to InsightFlow (telemetry)
└── Continue with normal startup (DB init, Prometheus, etc.)
```

## Service Discovery

Services are discovered via environment variables:

| Service | Env Var | Default | Purpose |
|---------|---------|---------|---------|
| BHIV Core | `BHIV_CORE_URL` | `http://localhost:8000` | Execution pipeline |
| Creator Core | `CREATOR_CORE_URL` | `http://localhost:8002` | Business logic |
| Prompt Runner | `PROMPT_RUNNER_URL` | `http://localhost:8001` | LLM prompt execution |
| Bucket | `BUCKET_SERVICE_URL` | `http://localhost:8003` | Content storage |
| InsightFlow | `INSIGHTFLOW_URL` | `http://localhost:8004` | Analytics & telemetry |
| TANTRA Runtime | `TANTRA_RUNTIME_URL` | `http://localhost:8005` | Execution infrastructure |

## Health Check

```bash
GET /integration/health
```

Returns connectivity status for all services:

```json
{
  "status": "healthy",
  "configured_services": 3,
  "total_services": 6,
  "services": {
    "bhiv_core": {"available": true, "url": "http://localhost:8000"},
    "prompt_runner": {"available": false},
    "insightflow": {"available": true}
  }
}
```

## Registration

### TANTRA Runtime
Registers platform capabilities and startup metadata:
```json
{
  "platform_id": "ai_content_platform",
  "version": "1.0.0",
  "capabilities": ["content_upload", "video_generation", "feedback_learning"]
}
```

### BHIV Core
Registers platform identity and execution contract:
```json
{
  "platform_id": "ai_content_platform",
  "schema_version": "1.0.0",
  "execution_mode": "standalone"
}
```

### InsightFlow
Emits startup telemetry event with integration status.

## Standalone Mode

When no external services are configured, the platform operates in standalone mode:
- All local implementations are used as fallbacks
- No external HTTP calls are made
- All existing functionality remains available
- Logs indicate standalone operation

## Configuration Validation

```bash
GET /integration/status
```

Returns which adapters are configured vs missing:
```json
{
  "status": "ok",
  "adapters": {
    "bhiv_core": {"configured": true, "available": true},
    "prompt_runner": {"configured": false, "available": false}
  },
  "config": {
    "total_configured": 2,
    "total_missing": 4
  }
}
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| All services show unavailable | Verify env vars in `.env` file |
| TANTRA registration fails | Ensure TANTRA Runtime is running |
| InsightFlow events not appearing | Check `INSIGHTFLOW_URL` and network |
| Platform won't start | Check logs for import errors in `core/integration/` |

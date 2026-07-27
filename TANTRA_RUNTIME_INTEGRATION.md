# TANTRA Runtime Integration

## Overview
The AI Content Platform registers with TANTRA Runtime as an execution participant, enabling delegated execution of content processing tasks through the canonical BHIV execution infrastructure.

## Registration

On startup, the platform registers with TANTRA:

```python
await integration_manager.tantra.register({
    "platform_id": "ai_content_platform",
    "version": "1.0.0",
    "phase": "IV",
    "capabilities": ["content_upload", "video_generation", "feedback_learning"],
    "startup_time": "2026-07-26 12:00:00"
})
```

## Execution Model

```
User Request
  ↓
AI Content Platform (receives request)
  ↓
TANTRA Runtime (execution orchestrator)
  ↓
BHIV Core (processes via modules)
  ↓
Prompt Runner (LLM execution)
  ↓
Creator Core (business logic)
  ↓
Bucket (storage)
  ↓
InsightFlow (telemetry)
  ↓
Response to User
```

## Fallback Chain

Each adapter follows the same pattern:

1. **Check availability**: `adapter.is_available()` checks if URL is configured
2. **Try external service**: HTTP call to external service
3. **Fall back to local**: If external unavailable, use local implementation
4. **Never fail caller**: External service errors are logged, not raised

```python
# Canonical fallback pattern
if integration_manager.tantra.is_available():
    result = await integration_manager.tantra.execute(...)
else:
    result = local_implementation()
```

## Adapter Classes

### BHIVCoreAdapter
- `execute(trace_id, module, action, payload)` — Execute module action
- `register(platform_id, metadata)` — Register platform
- `notify(event_type, data)` — Send notifications

### PromptRunnerAdapter
- `execute(prompt, context, model)` — Execute prompt via Prompt Runner
- `register(prompt_id, metadata)` — Register prompt template

### BucketAdapter
- `upload(file_data, filename)` — Upload to Bucket
- `download(file_id)` — Download from Bucket
- `get_presigned_url(file_id)` — Get presigned URL

### InsightFlowAdapter
- `emit(event_type, data, user_id)` — Emit telemetry event
- `track(metric_name, value)` — Track custom metric

### TANTRAAdapter
- `register(metadata)` — Register with TANTRA Runtime
- `execute(operation, payload)` — Execute via TANTRA

### CreatorCoreAdapter
- `execute(action, payload)` — Execute business logic
- `register(platform_id, metadata)` — Register platform

## Environment Variables

```env
# Required for external service routing
BHIV_CORE_URL=http://localhost:8000
PROMPT_RUNNER_URL=http://localhost:8001
CREATOR_CORE_URL=http://localhost:8002
BUCKET_SERVICE_URL=http://localhost:8003
INSIGHTFLOW_URL=http://localhost:8005
TANTRA_RUNTIME_URL=http://localhost:8006

# API Keys (if required by services)
BHIV_CORE_API_KEY=your-key
PROMPT_RUNNER_API_KEY=your-key
CREATOR_CORE_API_KEY=your-key
BUCKET_SERVICE_API_KEY=your-key
INSIGHTFLOW_API_KEY=your-key
TANTRA_RUNTIME_API_KEY=your-key

# Timeouts (seconds)
BHIV_CORE_TIMEOUT=30
PROMPT_RUNNER_TIMEOUT=60
CREATOR_CORE_TIMEOUT=30
BUCKET_SERVICE_TIMEOUT=60
INSIGHTFLOW_TIMEOUT=10
TANTRA_RUNTIME_TIMEOUT=30
```

## Trace Propagation

All external calls propagate `trace_id` for end-to-end observability:

```python
result = await integration_manager.bhiv_core.execute(
    trace_id="trace_1234567890",
    module="storyboard",
    action="process",
    payload={...}
)
```

The `trace_id` is preserved through:
- BHIV Core → Prompt Runner → Creator Core → Bucket → InsightFlow
- All telemetry events include the same `trace_id`
- Errors are logged with the originating `trace_id`

## Non-Blocking Design

All external calls are wrapped in try/except:

```python
try:
    result = await adapter.execute(...)
except Exception as e:
    logger.debug("External service unavailable, using local: %s", e)
    result = local_implementation()
```

This ensures:
- Platform starts even if external services are down
- Platform continues operating if external services fail mid-request
- No cascade failures from external service issues
- Graceful degradation to local implementations

## Monitoring

```bash
# Check integration health
GET /integration/health

# Check adapter status
GET /integration/status

# Check specific service connectivity
GET /health
```

# Trace Flow Documentation

## Overview
The AI Content Platform propagates `trace_id` end-to-end through the BHIV ecosystem for distributed tracing and debugging.

## Trace Propagation Path

```
User Request
  │  trace_id: "trace_1234567890"
  ↓
AI Content Platform (app/routes.py)
  │  trace_id preserved in request context
  ↓
BHIV Core Adapter (core/bhiv_core.py)
  │  trace_id sent to external BHIV Core
  ↓
Prompt Runner Adapter (core/bhiv_lm_client.py)
  │  trace_id sent to external Prompt Runner
  ↓
Creator Core Adapter (core/integration/adapters.py)
  │  trace_id sent to external Creator Core
  ↓
Bucket Adapter (core/integration/adapters.py)
  │  trace_id sent to external Bucket
  ↓
InsightFlow Adapter (app/observability.py)
  │  trace_id emitted with telemetry events
  ↓
Response to User
  │  trace_id returned in response headers
```

## Trace ID Generation

```python
# Generated at request entry
trace_id = f"trace_{int(time.time()*1000)}"

# Example: trace_1722000000000
```

## Trace Propagation in Adapters

Each adapter propagates `trace_id` in HTTP headers:

```python
headers = {
    "X-Trace-ID": trace_id,
    "X-Platform-ID": "ai_content_platform",
    "X-Schema-Version": "1.0.0",
    "Authorization": f"Bearer {api_key}"
}
```

## Trace in Observability

### PostHog Events
```python
posthog_manager.track_event(user_id, "content_uploaded", {
    "trace_id": trace_id,
    "content_id": content_id
})
```

### InsightFlow Events
```python
await integration_manager.insightflow.emit(
    event_type="content_uploaded",
    data={
        "trace_id": trace_id,
        "content_id": content_id,
        "user_id": user_id
    },
    user_id=user_id
)
```

### Sentry Errors
```python
sentry_sdk.set_tag("trace_id", trace_id)
sentry_sdk.capture_exception(error)
```

## Trace in Error Handling

```python
try:
    result = await external_service.execute(trace_id=trace_id, ...)
except Exception as e:
    logger.error("Service failed [trace=%s]: %s", trace_id, e)
    # Fallback to local implementation
    result = local_implementation()
```

## Trace in Logs

All structured logs include `trace_id`:

```json
{
  "event": "content_processed",
  "trace_id": "trace_1722000000000",
  "user_id": "user_123",
  "timestamp": "2026-07-26T12:00:00Z"
}
```

## Trace Propagation Middleware

The `TracePropagationMiddleware` in `app/platform_contract.py` automatically:
1. Extracts `trace_id` from request headers
2. Injects `trace_id` into request state
3. Adds `trace_id` to response headers
4. Logs trace events for observability

## Endpoints That Propagate Trace

| Endpoint | Trace Source | Trace Propagation |
|----------|--------------|-------------------|
| `POST /upload` | Request header | BHIV Core → Prompt Runner → Bucket |
| `POST /process` | Request header | BHIV Core → Creator Core |
| `POST /feedback` | Request header | BHIV Core → InsightFlow |
| `GET /content/{id}` | Request header | Bucket → InsightFlow |
| `POST /webhook` | Request header | BHIV Core → Prompt Runner → Bucket |

## Debugging with Trace ID

### Find request in logs
```bash
grep "trace_1722000000000" logs/app.log
```

### Find request in PostHog
```sql
SELECT * FROM events WHERE properties->>'trace_id' = 'trace_1722000000000'
```

### Find request in InsightFlow
```bash
GET /insightflow/events?trace_id=trace_1722000000000
```

### Find request in Sentry
```bash
# Search by trace_id tag
trace_id:trace_1722000000000
```

## Trace ID Format

```
trace_{timestamp_ms}

Example: trace_1722000000000
         └── 13 digits (milliseconds since epoch)
```

## Best Practices

1. **Always propagate trace_id** — Never drop trace context
2. **Log with trace_id** — Include in all structured logs
3. **Tag errors with trace_id** — Set in Sentry tags
4. **Return trace_id to user** — Include in response headers
5. **Never log sensitive data** — Trace ID is safe, but PII is not

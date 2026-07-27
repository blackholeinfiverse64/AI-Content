# Deployment Runtime Configuration

## Overview
The AI Content Platform supports both standalone and ecosystem-connected deployment modes. This document covers runtime configuration for BHIV ecosystem integration.

## Deployment Modes

### Standalone Mode (Default)
- No external services configured
- All processing uses local implementations
- No HTTP calls to external services
- Full functionality with local fallbacks

### Ecosystem Mode
- External services configured via environment variables
- Requests routed through BHIV Core → Prompt Runner → Creator Core
- Telemetry emitted to InsightFlow
- TANTRA Runtime manages execution

## Environment Variables

### Required for Ecosystem Mode

```env
# Platform Identity
PLATFORM_ID=ai_content_platform
PLATFORM_SCHEMA_VERSION=1.0.0

# BHIV Core (Execution Pipeline)
BHIV_CORE_URL=http://localhost:8000
BHIV_CORE_API_KEY=your-api-key
BHIV_CORE_TIMEOUT=30

# Prompt Runner (LLM Execution)
PROMPT_RUNNER_URL=http://localhost:8001
PROMPT_RUNNER_API_KEY=your-api-key
PROMPT_RUNNER_TIMEOUT=60

# Creator Core (Business Logic)
CREATOR_CORE_URL=http://localhost:8002
CREATOR_CORE_API_KEY=your-api-key
CREATOR_CORE_TIMEOUT=30

# Bucket (Content Storage)
BUCKET_SERVICE_URL=http://localhost:8003
BUCKET_SERVICE_API_KEY=your-api-key
BUCKET_SERVICE_TIMEOUT=60

# InsightFlow (Analytics & Telemetry)
INSIGHTFLOW_URL=http://localhost:8005
INSIGHTFLOW_API_KEY=your-api-key
INSIGHTFLOW_TIMEOUT=10

# TANTRA Runtime (Execution Infrastructure)
TANTRA_RUNTIME_URL=http://localhost:8006
TANTRA_RUNTIME_API_KEY=your-api-key
TANTRA_RUNTIME_TIMEOUT=30
```

### Required for All Modes

```env
# Database
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_content_platform

# Authentication
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Observability
SENTRY_DSN=your-sentry-dsn
POSTHOG_API_KEY=your-posthog-key
```

## Deployment Platforms

### Render.com
```yaml
# render.yaml
services:
  - type: web
    name: ai-content-platform
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PLATFORM_ID
        value: ai_content_platform
      - key: BHIV_CORE_URL
        sync: false
      - key: PROMPT_RUNNER_URL
        sync: false
```

### Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  ai-content-platform:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PLATFORM_ID=ai_content_platform
      - BHIV_CORE_URL=http://bhiv-core:8000
      - PROMPT_RUNNER_URL=http://prompt-runner:8001
      - BUCKET_SERVICE_URL=http://bucket:8003
      - INSIGHTFLOW_URL=http://insightflow:8005
      - TANTRA_RUNTIME_URL=http://tantra-runtime:8006
    depends_on:
      - mongodb
      - bhiv-core
      - prompt-runner
      - bucket
      - insightflow
      - tantra-runtime
```

## Health Checks

### Application Health
```bash
GET /health
```

### Integration Health
```bash
GET /integration/health
```

### Integration Status
```bash
GET /integration/status
```

## Monitoring

### Prometheus Metrics
```bash
GET /metrics/prometheus
```

### Observability Dashboard
```bash
GET /observability/dashboard
```

### Performance Metrics
```bash
GET /observability/metrics/performance
```

## Troubleshooting

### Service Unavailable
1. Check environment variables in `.env`
2. Verify service URLs are correct
3. Check network connectivity
4. Review service logs for errors

### Registration Failed
1. Check TANTRA Runtime is running
2. Verify API key is valid
3. Review startup logs for errors

### Telemetry Not Appearing
1. Check InsightFlow URL
2. Verify API key
3. Check network connectivity
4. Review InsightFlow logs

## Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **Network**: Use HTTPS in production
3. **Timeouts**: Set appropriate timeouts to prevent hanging
4. **Retry**: Use exponential backoff for retries
5. **Circuit Breaking**: Use circuit breakers for external calls

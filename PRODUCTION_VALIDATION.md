# Production Validation Checklist

## Overview
This document provides a checklist for validating the AI Content Platform in production with BHIV ecosystem integration.

## Pre-Deployment Checklist

### Environment Variables
- [ ] `PLATFORM_ID` set to `ai_content_platform`
- [ ] `PLATFORM_SCHEMA_VERSION` set to `1.0.0`
- [ ] `BHIV_CORE_URL` configured
- [ ] `BHIV_CORE_API_KEY` configured
- [ ] `PROMPT_RUNNER_URL` configured
- [ ] `PROMPT_RUNNER_API_KEY` configured
- [ ] `CREATOR_CORE_URL` configured
- [ ] `CREATOR_CORE_API_KEY` configured
- [ ] `BUCKET_SERVICE_URL` configured
- [ ] `BUCKET_SERVICE_API_KEY` configured
- [ ] `INSIGHTFLOW_URL` configured
- [ ] `INSIGHTFLOW_API_KEY` configured
- [ ] `TANTRA_RUNTIME_URL` configured
- [ ] `TANTRA_RUNTIME_API_KEY` configured
- [ ] `MONGODB_URL` configured
- [ ] `JWT_SECRET_KEY` configured
- [ ] `SENTRY_DSN` configured
- [ ] `POSTHOG_API_KEY` configured

### Service Connectivity
- [ ] BHIV Core reachable
- [ ] Prompt Runner reachable
- [ ] Creator Core reachable
- [ ] Bucket reachable
- [ ] InsightFlow reachable
- [ ] TANTRA Runtime reachable
- [ ] MongoDB reachable

### Security
- [ ] HTTPS enabled
- [ ] API keys stored securely
- [ ] JWT tokens working
- [ ] Rate limiting configured
- [ ] Input validation enabled
- [ ] File type restrictions enforced

## Deployment Validation

### Step 1: Start Application
```bash
# Check startup logs
docker logs ai-content-platform

# Verify startup events
grep "Application starting" logs/app.log
grep "TANTRA registration" logs/app.log
grep "BHIV Core registration" logs/app.log
```

### Step 2: Health Checks
```bash
# Basic health
curl http://localhost:8000/health

# Integration health
curl http://localhost:8000/integration/health

# Integration status
curl http://localhost:8000/integration/status
```

### Step 3: Authentication
```bash
# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Verify token
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <token>"
```

### Step 4: Content Upload
```bash
# Upload video
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test-video.mp4"

# Upload script
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test-script.txt"
```

### Step 5: Processing
```bash
# Process content
curl -X POST http://localhost:8000/process \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "<content_id>"}'

# Check processing status
curl http://localhost:8000/content/<content_id> \
  -H "Authorization: Bearer <token>"
```

### Step 6: Feedback
```bash
# Submit feedback
curl -X POST http://localhost:8000/feedback \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "<content_id>", "rating": 5, "comment": "Great content!"}'
```

### Step 7: Observability
```bash
# Dashboard
curl http://localhost:8000/observability/dashboard

# Metrics
curl http://localhost:8000/observability/metrics/performance

# Trace
curl http://localhost:8000/observability/trace/<trace_id>
```

## Ecosystem Integration Validation

### Step 1: TANTRA Registration
```bash
# Check TANTRA registration
curl http://localhost:8000/integration/health | jq '.services.tantra'

# Expected output:
# {
#   "available": true,
#   "url": "http://localhost:8006",
#   "last_check": "2026-07-26T12:00:00Z"
# }
```

### Step 2: BHIV Core Routing
```bash
# Process content (should route through BHIV Core)
curl -X POST http://localhost:8000/process \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "<content_id>"}'

# Check logs for BHIV Core routing
grep "External BHIV Core" logs/app.log
```

### Step 3: Prompt Runner Routing
```bash
# Generate storyboard (should route through Prompt Runner)
curl -X POST http://localhost:8000/process \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"content_id": "<content_id>", "action": "generate_storyboard"}'

# Check logs for Prompt Runner routing
grep "External Prompt Runner" logs/app.log
```

### Step 4: InsightFlow Telemetry
```bash
# Check InsightFlow events
curl http://localhost:8005/events?platform=ai_content_platform

# Expected events:
# - platform_startup
# - content_uploaded
# - content_processed
# - storyboard_generated
```

### Step 5: Bucket Storage
```bash
# Upload to Bucket
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test-video.mp4"

# Check Bucket
curl http://localhost:8003/files?platform=ai_content_platform
```

## Performance Validation

### Response Times
- [ ] Health check < 100ms
- [ ] Integration health < 500ms
- [ ] Content upload < 5s
- [ ] Processing < 30s
- [ ] Feedback submission < 1s

### Throughput
- [ ] Concurrent uploads: 10+
- [ ] Concurrent processing: 5+
- [ ] Concurrent feedback: 20+

### Resource Usage
- [ ] Memory < 512MB
- [ ] CPU < 50%
- [ ] Disk < 1GB
- [ ] Network < 100MB/hour

## Rollback Plan

### If Integration Fails
1. Set all service URLs to empty
2. Restart application
3. Platform will operate in standalone mode
4. All local fallbacks will be used

### If Application Fails
1. Check logs for errors
2. Verify environment variables
3. Check service connectivity
4. Restart application

### If Database Fails
1. Check MongoDB connectivity
2. Verify database credentials
3. Check disk space
4. Restart MongoDB

## Post-Deployment Monitoring

### Daily Checks
- [ ] Integration health status
- [ ] Error rates
- [ ] Response times
- [ ] Resource usage

### Weekly Checks
- [ ] Telemetry data quality
- [ ] Performance trends
- [ ] Security alerts
- [ ] Backup verification

### Monthly Checks
- [ ] Service updates
- [ ] Security patches
- [ ] Performance optimization
- [ ] Documentation updates

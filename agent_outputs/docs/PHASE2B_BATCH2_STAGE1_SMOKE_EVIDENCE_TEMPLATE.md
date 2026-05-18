# Phase 2B Batch2 Stage1 Smoke Evidence Template

Status: STAGE1 DOCS/TEST TRACKING TEMPLATE
Date: 2026-05-17
Owner: Docs/Test Agent
Scope: Batch2 Stage1 evidence capture for existing Batch1-compatible runtime lanes.

## 0. Scope Guard

This template is for evidence capture only.

Forbidden:
- no business code changes;
- no model weight changes;
- no video/realtime/Word/dashboard/large-screen scope;
- no breaking change to `detection_result.v1`;
- no Batch2 implementation authorization is implied.

## 1. Stage1 Gate Summary

```text
Phase 2B Batch2 Stage1: EVIDENCE COLLECTION PENDING
Batch1 baseline: FULL PASS CANDIDATE
Implementation status: NOT STARTED BY DOCS/TEST
Compatibility gate: detection_result.v1 MUST remain backward compatible
```

## 2. Required Evidence Slots

| Evidence slot | Required source | Current status | PASS condition | Evidence to paste |
|---|---|---|---|---|
| backend pytest | Backend Agent | WAITING | pytest exits 0; failures = 0 | command, exit code, summary, warnings count |
| frontend build | Frontend Agent | WAITING | build exits 0 | command, exit code, build summary |
| runtime diagnostics | Backend/AI Agents | WAITING | runtime confirms dependency/weight/service readiness | ultralytics version, weight path/hash/size, service health |
| image detection response | Backend/AI Agents | WAITING | `/api/detection/image` returns HTTP 200 and `code=0` using real runtime path | request summary and sanitized JSON response |
| result image URL | Backend/Frontend Agents | WAITING | result image URL/object key exists and is retrievable under expected auth rules | URL/object key, status code, content metadata |
| records detail | Backend/Frontend Agents | WAITING | generated detection record detail is readable and contains `detection_result.v1` | record ID, detail JSON snippet |

## 3. Evidence Capture Blocks

### 3.1 Backend pytest

```text
Source agent:
Worktree:
Branch:
Commit:
Command:
Exit code:
Result summary:
Warnings:
Raw log location or excerpt:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

### 3.2 Frontend build

```text
Source agent:
Worktree:
Branch:
Commit:
Command:
Exit code:
Build result:
Warnings:
Raw log location or excerpt:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

### 3.3 Runtime diagnostics

```text
Source agent:
Backend service status:
AI dependency version:
Weight filename:
Weight resolved path:
Weight size:
Weight SHA256:
/api/models/published weight_exists:
Runtime diagnostic command/log:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

### 3.4 Image detection response

```text
Source agent:
Request endpoint:
Request image/test asset:
Threshold/config:
HTTP status:
Response code:
record_id:
detection_result.schema_version:
detection count:
Sanitized response excerpt:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

### 3.5 Result image URL

```text
Source agent:
record_id:
result_image.url or object_key:
Access mode/token status:
HTTP status:
Content-Type:
Content-Length or file size:
Screenshot/artifact path if available:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

### 3.6 Records detail

```text
Source agent:
record_id:
Detail endpoint:
HTTP status:
Response code:
detection_result.schema_version:
detection count:
Original/result image fields present:
Sanitized detail excerpt:
Docs/Test status: WAITING / PASS / FAIL / BLOCKED
```

## 4. Stage1 Decision Template

```text
Phase 2B Batch2 Stage1 Smoke: PASS / PARTIAL PASS / FAIL / BLOCKED / WAITING
Decision date:
Decision owner:
Evidence summary:
- backend pytest:
- frontend build:
- runtime diagnostics:
- image detection response:
- result image URL:
- records detail:
Remaining blockers:
- 
Scope guard respected: YES / NO
Business code modified by Docs/Test: NO
Weights modified by Docs/Test: NO
Video/realtime/Word/dashboard scope entered: NO
```

## 5. Append-only Rule

When Stage1 smoke evidence arrives, append a dated update below. Do not overwrite previous evidence or Batch1 history.

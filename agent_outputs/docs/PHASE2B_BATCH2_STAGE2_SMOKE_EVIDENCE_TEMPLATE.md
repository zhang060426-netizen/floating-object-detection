# Phase 2B Batch2 Stage2 Smoke Evidence Template

Status: TEMPLATE - WAITING FOR SMOKE EVIDENCE
Date: 2026-05-18
Owner: Docs/Test Agent
Scope: Stage2 evidence capture for Backend / Frontend / AI smoke outputs.

## 0. Scope Guard

Stage2 evidence capture does not authorize:
- Batch3;
- video detection;
- realtime/camera detection;
- Word report export;
- dashboard or large-screen work;
- model training or weight replacement;
- business code changes by Docs/Test;
- breaking changes to `detection_result.v1`.

## 1. Evidence Metadata

| Field | Value |
|---|---|
| Evidence provider | Backend / Frontend / AI / Docs-Test |
| Worktree |  |
| Branch |  |
| Commit |  |
| Date/time |  |
| Command(s) run |  |
| Exit code(s) |  |
| Attachments / logs |  |

## 2. Required Stage2 Evidence Slots

| Requested slot | Expected | Result | Evidence |
|---|---|---|---|
| Backend API smoke | Login/model/image detection/result image/record detail path passes | WAITING / PASS / FAIL / BLOCKED |  |
| Frontend build | Build exits 0 | WAITING / PASS / FAIL / BLOCKED |  |
| Frontend UI/API smoke | Login + image detection UI/API flow does not crash and remains response-compatible | WAITING / PASS / FAIL / BLOCKED |  |
| AI unittest | AI unittest exits 0 with no failures | WAITING / PASS / FAIL / BLOCKED |  |
| AI readiness hash | Approved smoke weight exists/readable and hash recorded/matches expected or approved hash | WAITING / PASS / FAIL / BLOCKED |  |
| `detection_result.v1` compatibility | Stage2 smoke evidence preserves `detection_result.v1` | WAITING / PASS / FAIL / BLOCKED |  |
| Forbidden scope guard | No Batch3/video/realtime/Word/dashboard/business-code/weight changes by Docs/Test | PASS / FAIL / BLOCKED |  |
| Final PASS/FAIL/BLOCKED | Final state selected only after all smoke evidence is complete or a specific fail/blocker is proven | WAITING / PASS / FAIL / BLOCKED |  |

## 3. Backend Evidence Detail

| Slot | Expected | Result | Evidence |
|---|---|---|---|
| Backend API smoke | combined backend API smoke passes | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Login/auth | HTTP 200, `code=0`, token/session available | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Model readiness | published model/runtime readiness visible | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Image detection | HTTP 200, `code=0` | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Result image | retrievable image bytes/content type | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Record detail | readable record with `detection_result.v1` | WAITING / PASS / FAIL / BLOCKED / N/A |  |

## 4. Frontend Evidence Detail

| Slot | Expected | Result | Evidence |
|---|---|---|---|
| Frontend build | build exits 0 | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Frontend UI/API smoke | UI/API flow does not crash | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Login display | login flow does not crash | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Image detection display | upload/result path does not crash | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Result image display | generated result image displays or clear fallback shown | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Record detail display | `detection_result.v1` record renders without schema failure | WAITING / PASS / FAIL / BLOCKED / N/A |  |

## 5. AI Evidence Detail

| Slot | Expected | Result | Evidence |
|---|---|---|---|
| AI unittest | unittest exits 0 with no failures | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| AI readiness hash | approved smoke weight exists/readable/hash recorded | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Dependency | `ultralytics` import/version available | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Default inference | backend image detection path succeeds | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Output schema | `detection_result.v1` preserved | WAITING / PASS / FAIL / BLOCKED / N/A |  |
| Result image | generated output is readable | WAITING / PASS / FAIL / BLOCKED / N/A |  |

## 6. Compatibility Statement

```text
API envelope changed: No / Yes / Unknown
DB schema changed: No / Yes / Unknown
JWT fields changed: No / Yes / Unknown
File storage contract changed: No / Yes / Unknown
Model weights changed: No / Yes / Unknown
detection_result.v1 preserved: Yes / No / Unknown
Forbidden scope entered: No / Yes / Unknown
```

## 7. Decision

```text
Stage2 evidence status: WAITING / PASS / FAIL / BLOCKED
Reason:
Final PASS declared: No / Yes
Batch3 entered: No / Yes
Video/realtime/Word/dashboard entered: No / Yes
Weight modified: No / Yes
detection_result.v1 broken: No / Yes / Unknown
```

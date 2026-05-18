# Phase 2B Batch2 Stage2 Closeout Criteria

Status: ACTIVE CRITERIA - NOT CLOSED
Date: 2026-05-18
Owner: Docs/Test Agent

## 1. Closeout States

Stage2 closeout must select exactly one final state:

- PASS: all required Backend, Frontend, AI, and Docs/Test evidence slots pass.
- FAIL: evidence was executed and at least one required slot violates expected behavior.
- BLOCKED: required evidence cannot be collected due to missing service, missing logs, missing authorization, or environment issue.

Until one state is justified, Stage2 remains `WAITING FOR EVIDENCE`.

## 2. PASS Requirements

All items must be true before Stage2 PASS:

| Requirement | Required evidence |
|---|---|
| Backend smoke PASS | pytest plus login/model/image detection/result image/record detail evidence |
| Frontend smoke PASS | build plus display compatibility evidence |
| AI smoke/readiness PASS | dependency, weight readiness, inference compatibility, schema evidence |
| `detection_result.v1` preserved | response/detail JSON snippet or explicit smoke output |
| No weight mutation | hash/metadata comparison or explicit no-change evidence |
| No forbidden scope entered | explicit statement covering Batch3/video/realtime/Word/dashboard |
| Docs/Test artifacts updated | Stage2 template/tracking/checklist updated |

## 3. FAIL Conditions

Any confirmed item below produces Stage2 FAIL unless corrected and re-smoked:

- Backend tests fail.
- Frontend build fails.
- `ultralytics` is unavailable when required by smoke.
- Approved smoke weight is missing/unreadable without authorized replacement.
- `/api/detection/image` does not return Batch1/Stage1-compatible success for required test input.
- Result image is missing or unreadable.
- Auto-save record is missing or unreadable.
- `detection_result.v1` is broken or migrated without authorization.
- Frontend crashes on Stage2-compatible response.

## 4. BLOCKED Conditions

Use BLOCKED rather than FAIL when evidence cannot be collected:

- Smoke environment is unavailable.
- Required service cannot be started within authorized scope.
- Required smoke output/log is not provided to Docs/Test.
- Authorization is missing for a required operation.
- Evidence is ambiguous and cannot be safely inferred.

## 5. Non-entry Requirements

Stage2 closeout must explicitly state:

```text
Batch3: NOT ENTERED / NOT AUTHORIZED
Video detection: NOT ENTERED
Realtime/camera detection: NOT ENTERED
Word report export: NOT ENTERED
Dashboard/large-screen: NOT ENTERED
Model weights: NOT MODIFIED unless separately authorized
detection_result.v1: PRESERVED or BLOCK/FAIL
```

## 6. Rollback / Recovery Note

Docs/Test Stage2 artifacts are documentation-only. If rollback is required, revert Stage2 docs/task artifacts independently. Do not touch business code, runtime database files, generated smoke images, or model weights from Docs/Test rollback.

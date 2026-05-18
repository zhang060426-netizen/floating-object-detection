# Phase 2B Batch2 Smoke Test Plan

Status: PLANNING ARTIFACT ONLY
Date: 2026-05-17
Scope: Batch2 planning smoke coverage for existing Batch1-compatible runtime lanes.

## 0. Gate Boundary

This smoke plan does not start Batch2 implementation.

Forbidden during this plan:
- no business-code changes;
- no model weight changes;
- no video/realtime/Word/dashboard/large-screen scope;
- no breaking change to `detection_result.v1`.

## 1. Frozen Starting Point

Batch1 is currently `FULL PASS CANDIDATE` based on the latest smoke report:

- `ultralytics=8.4.51` available.
- `yolo26n.pt` exists, readable, size `5,544,453 bytes`.
- `yolo26n.pt` SHA256 `9b09cc8bf347f0fc8a5f7657480587f25db09b34bf33b0652110fb03a8ad4fef`.
- `/api/models/published` returns `weight_exists=true`.
- `/api/detection/image` returns HTTP 200 and `code=0`.
- Auto-generated record `dr_6d855b7125c84813bc794e946411ac13` exists.
- Low-threshold record `dr_227020535354488a99b3703c07b62449` has detection count `1`.
- Result image generated, size `131182 bytes`.
- `detection_result.schema_version=detection_result.v1`.
- pytest result: `4 passed, 25 warnings`.
- Frontend build and display compatibility passed.

## 2. Smoke Groups

### 2.1 Backend API Smoke

| ID | Area | Action | Expected result | Evidence |
|---|---|---|---|---|
| B2-BE-HEALTH-01 | Health | `GET /api/health` | HTTP 200, `code=0`, healthy status | command + JSON summary |
| B2-BE-AUTH-01 | Auth | login with frozen admin account | HTTP 200, token returned | sanitized response |
| B2-BE-MODEL-01 | Models | `GET /api/models/published` | model returned with `weight_exists=true` | JSON snippet |
| B2-BE-DETECT-01 | Detection | authenticated image upload | HTTP 200, `code=0` | request summary + response snippet |
| B2-BE-FILE-01 | File | fetch generated result image URL | HTTP 200, readable image bytes | URL + metadata |
| B2-BE-REC-01 | Records | list/detail generated record | HTTP 200, record contains detection result | record ID + JSON snippet |

### 2.2 AI Runtime Smoke

| ID | Area | Action | Expected result | Evidence |
|---|---|---|---|---|
| B2-AI-DEP-01 | Dependency | import/version check | `ultralytics=8.4.51` or approved compatible version | command output |
| B2-AI-WEIGHT-01 | Weight | file exists/read/hash | expected size/hash or approved update | file metadata |
| B2-AI-INF-01 | Inference | default-threshold image inference via backend path | success response with `detection_result.v1` | API output |
| B2-AI-INF-02 | Low threshold | threshold `0.10` smoke | detection count >= 1 when expected test image is used | record/detail output |
| B2-AI-IMG-01 | Result image | output image generated | non-zero bytes, readable | file metadata |

### 2.3 Frontend Smoke

| ID | Area | Action | Expected result | Evidence |
|---|---|---|---|---|
| B2-FE-BUILD-01 | Build | run frontend build | exit code 0 | build log |
| B2-FE-AUTH-01 | Login | login page flow | successful token/session state | screenshot/network summary |
| B2-FE-DETECT-01 | Detection page | upload image and display result | no crash; summary/result image visible | screenshot/network summary |
| B2-FE-REC-01 | Records | show generated detection record if UI supports it | record detail compatible with `detection_result.v1` | screenshot/network summary |
| B2-FE-ERR-01 | Error display | simulate/observe backend error state | user-visible non-crashing error | screenshot/log |

### 2.4 Docs/Test Smoke

| ID | Area | Action | Expected result | Evidence |
|---|---|---|---|---|
| B2-DOC-ART-01 | Artifacts | verify all Batch2 planning files exist | 7 required files present | file list |
| B2-DOC-SCOPE-01 | Scope | confirm no business code/weights changed by docs task | only docs/tasks files changed plus runtime `.omx` if present | git status |
| B2-DOC-SCHEMA-01 | Compatibility | verify docs keep `detection_result.v1` compatibility gate | explicit compatibility clause exists | grep/result |

## 3. PASS / FAIL / BLOCKED Rules

- PASS: expected result has direct evidence.
- FAIL: command/API/build runs and violates expected result.
- BLOCKED: cannot execute due to missing service, missing artifact, missing authorization, or environment issue.
- N/A: out of scope by frozen Batch2 planning boundary.

## 4. Batch2 Non-goals

The following must remain N/A unless Leader explicitly changes scope:

- video detection;
- realtime/camera detection;
- Word report export;
- dashboard/large-screen polish;
- model training or weight replacement;
- schema-breaking `detection_result.v2` migration.

## 5. Report Destination

Future Batch2 runtime smoke results should be appended to a dedicated report, for example:

```text
agent_outputs/docs/PHASE2B_BATCH2_SMOKE_TEST_REPORT.md
```

Do not overwrite Batch1 smoke history.

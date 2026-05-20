# Phase 2B Batch4 Evaluation / Performance Test Plan

Status: PLANNING ONLY  
Date: 2026-05-20  
Owner: Docs/Test Agent  
Project: 水面漂浮物垃圾检测系统  
Scope: Batch4 Docs/Test planning gate for future evaluation and performance acceptance.  

> This document is a **planning artifact only**. It does not start Batch4 implementation, does not modify business code, does not train or replace models, and does not claim that any future evaluation/performance checks have passed.

## 0. Context Recovery

### 0.1 Latest stable baseline

| Item | Recovered state |
|---|---|
| Phase 2B Batch3 | CLOSED / ARCHIVED |
| Stable tag | `phase2b-batch3-docker-compose-stable` |
| Stable code point | `fddb0c8` |
| Archive commit | `ff731de` |
| Final Smoke Verification | PASS |
| Docker Compose deployment | PASS |
| `detection_result.v1` | PRESERVED |
| Runtime model mount | PASS |
| Batch4 state | PLANNING ONLY |

### 0.2 Local files inspected

Requested files/directories were inspected where present:

| Requested input | Local read result | Evidence level |
|---|---|---|
| `AGENTS.md` | Present; contains agent boundaries and no-business-code safety rules | Repository document confirmed |
| `PROJECT_CONTEXT.md` | Present; older context still describes broad project capabilities; treat as background, not current Batch4 fact | Repository document confirmed / historical context |
| `README.md` | Present; states current stage emphasizes planning and not large-scale implementation | Repository document confirmed |
| `tasks/docs/TASK_PHASE2B_BATCH4_PLANNING.md` | Not present in this worktree at planning time | Missing / pending source |
| `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md` | Not present in this worktree at planning time | Missing / pending source |
| `agent_outputs/docs/` | Present; Batch1-Batch3 docs and evidence files available | Repository artifact confirmed |
| `.omx/specs/` | Present; local planning/spec artifact available, but not a deliverable source of implementation fact | Local runtime/planning state |
| `.omx/plans/` | Present; local planning artifacts available, but not a deliverable source of implementation fact | Local runtime/planning state |

Because the two explicit Batch4 source files are absent, this plan uses the user's latest status block plus existing Batch3 closeout files as the authoritative Batch4 planning seed. Absence of those files is **not** treated as authorization to implement.

## 1. Batch4 Planning Gate Summary

### 1.1 Gate decision

```text
Phase 2B Batch4 Docs/Test Planning Gate: OPEN FOR PLANNING ONLY
Implementation authorization: NOT GRANTED
Business code changes: FORBIDDEN
Flask/Vue/YOLO logic changes: FORBIDDEN
Dockerfile / docker-compose.yml changes: FORBIDDEN
detection_result.v1 implementation changes: FORBIDDEN
Model weight/class/training changes: FORBIDDEN
Video/realtime/Word/dashboard/large-screen work: FORBIDDEN
Future implementation: REQUIRES SEPARATE EXPLICIT AUTHORIZATION
```

### 1.2 What Batch4 may produce now

Batch4 may produce planning documents that define future acceptance checks, evidence levels, and entry gates for later work. The current allowed deliverable is:

```text
agent_outputs/docs/PHASE2B_BATCH4_EVALUATION_TEST_PLAN.md
```

### 1.3 What Batch4 must not claim

Batch4 planning must not state or imply that:

- future model evaluation has already run;
- future performance tests have passed;
- video, realtime, Word export, dashboard, or large-screen features have been implemented or tested;
- `detection_result.v1` was changed or upgraded;
- model weights, classes, or training outputs were modified;
- Batch5+ implementation has started.

## 2. Future Evaluation Acceptance Checklist

The following checklist is for a **future authorized implementation/evaluation phase**. Each item remains `PLANNED`, not passed, until separately executed and evidenced.

### 2.1 Model / detection evaluation checklist

| Check item | Future acceptance evidence | Planned threshold / rule | Current Batch4 state |
|---|---|---|---|
| Dataset identity | Dataset path, split file, sample count, class list captured before run | Same dataset/split as declared by the authorized task; class `floating_object` preserved unless separately approved | PLANNED |
| Weight identity | Weight filename, checksum or immutable identifier, mount/source path | No silent replacement of stable runtime weight | PLANNED |
| Class compatibility | Class ID/name mapping captured | Preserve `class_id=0`, `floating_object` unless explicit cross-agent contract update exists | PLANNED |
| Inference config | `imgsz`, confidence threshold, IoU threshold, device, batch size recorded | Config must be reproducible | PLANNED |
| Core metrics | Precision, recall, mAP50, mAP50-95, false positives, false negatives | Thresholds must be set by the future authorized evaluation task before judging pass/fail | PLANNED |
| Sample-level audit | At least representative true positive / false positive / false negative examples archived | Must include input image ID and result artifact path | PLANNED |
| Regression comparison | Compare to prior stable baseline when available | Any regression must include cause/risk note | PLANNED |
| `detection_result.v1` compatibility | JSON sample before/after comparison | No breaking schema change without separate authorization | PLANNED |
| Error handling | Invalid image / missing model / empty detection cases documented | Expected response/error shape must be recorded | PLANNED |

### 2.2 API / persistence evaluation checklist

| Check item | Future acceptance evidence | Planned rule | Current Batch4 state |
|---|---|---|---|
| Health endpoint | Request/response capture | Service reachable in target runtime | PLANNED |
| Login/auth | Request/response capture, token field check | JWT contract must remain compatible | PLANNED |
| Image detection endpoint | Request/response capture with result artifact | Must return `detection_result.v1` compatible payload | PLANNED |
| Record save/read | DB/API evidence for generated `record_id` | Detection record roundtrip must be reproducible | PLANNED |
| File URL/path | Result image accessible via documented path/URL | No undocumented storage path break | PLANNED |
| Negative cases | Bad credentials, missing file, unsupported type | Expected error envelope documented | PLANNED |

## 3. Future Performance Acceptance Checklist

The following performance checks are **acceptance design only**. They require future authorization, environment declaration, and controlled execution before any PASS/FAIL claim.

### 3.1 Environment capture

| Required capture | Why it is required | Current Batch4 state |
|---|---|---|
| CPU/GPU model and driver/runtime | Performance is hardware-sensitive | PLANNED |
| OS, Python, Node, Docker versions | Runtime differences affect latency/build behavior | PLANNED |
| Model weight identity and device | Needed for reproducible inference timings | PLANNED |
| Dataset/test image list | Prevents cherry-picked timing data | PLANNED |
| Compose/native mode | Docker overhead must be distinguishable from native runtime | PLANNED |

### 3.2 Image detection performance

| Metric | Future measurement rule | Planned acceptance use |
|---|---|---|
| Cold start time | Time from service start to first successful health/detection | Deployment readiness signal |
| First inference latency | First image request after service start | Detects model load overhead |
| Warm inference latency | Median and p95 over a fixed image set | User-facing image detection responsiveness |
| Result artifact generation time | Time until result image path is available | End-to-end user flow timing |
| Record persistence latency | Time from detection completion to readable saved record | DB/API roundtrip health |
| Memory baseline/peak | Capture during cold load and repeated inference | Detects leaks or container sizing risk |

### 3.3 Future-only video/realtime performance gates

Video and realtime are explicitly **out of current Batch4 scope**. If a later authorized phase opens them, it must define separate gates before execution:

| Future area | Required pre-gate before any implementation/testing | Current Batch4 state |
|---|---|---|
| Video detection | Task status model, sampling strategy, keyframe retention rule, timeout policy, storage quota | NOT ENTERED |
| Realtime/camera | Camera source policy, FPS/latency target, dropped-frame rule, CPU/GPU budget, stop/reconnect behavior | NOT ENTERED |
| Word report export | Template contract, required fields, output path, missing-data behavior | NOT ENTERED |
| Dashboard/large-screen | Data refresh contract, chart source, performance budget, UI ownership | NOT ENTERED |

## 4. Evidence Level Update for Batch4+

Batch4+ planning should use the following evidence labels in addition to the existing evidence-level vocabulary.

| Evidence label | Definition | May be used to claim | Must not be used to claim |
|---|---|---|---|
| `PLANNED` | Requirement/checklist/gate has been defined but not executed | Future work shape exists | Test passed, implementation complete |
| `USER-PROVIDED STATUS` | Current status was provided by the user in the active instruction | Planning baseline for this session | Local git object/tag existence unless independently verified |
| `REPOSITORY ARTIFACT CONFIRMED` | File exists in this worktree and was read | Document/artifact content exists locally | Runtime behavior unless artifact contains verified runtime evidence |
| `MISSING / PENDING SOURCE` | Expected file is absent in this worktree | A planning input gap exists | That the missing file is unnecessary or superseded |
| `RUNTIME EVIDENCE ARCHIVED` | Prior evidence document records a PASS/FAIL with concrete scenario details | Historical archived result | Fresh run result for the current phase |
| `FUTURE VERIFICATION REQUIRED` | A check needs a later authorized run | A gate is required before implementation/closeout | Current phase has passed the check |

Required wording rule:

```text
Use "PLANNED" or "FUTURE VERIFICATION REQUIRED" for Batch4 evaluation/performance checks until a later authorized implementation/test phase executes them and archives evidence.
```

## 5. Batch5+ Preconditions

No Batch5+ work may start from this planning artifact alone. A future Batch5+ authorization must first satisfy all relevant preconditions below.

### 5.1 Authorization preconditions

- Explicit user/leader authorization naming the phase/batch and implementation scope.
- Written confirmation whether the scope includes only image detection or also video/realtime/Word/dashboard.
- Written confirmation if any shared contract may change.
- Separate authorization before touching weights, classes, training data, model files, or training code.

### 5.2 Contract preconditions

- `detection_result.v1` compatibility decision recorded.
- API request/response envelope changes, if any, documented before implementation.
- File storage path/URL behavior documented before changing persistence or result artifact logic.
- JWT/auth field impact documented before auth changes.
- Evaluation metrics schema documented before adding/changing model evaluation outputs.

### 5.3 Verification preconditions

- Stable rollback point identified.
- Test resources and expected smoke path listed.
- Acceptance thresholds defined before running evaluation/performance gates.
- Evidence capture template prepared.
- Scope guard reviewed for video/realtime/Word/dashboard exclusions or explicit inclusion.

### 5.4 Worktree / ownership preconditions

- Implementation agents use separate worktrees/branches.
- Docs/Test remains documentation/test owner and must not silently modify Frontend, Backend, or AI business logic.
- Cross-module changes require contract update and review before merge.

## 6. Maintained Forbidden Scope

The following remain forbidden in Batch4 planning:

- Do not modify backend business code.
- Do not modify frontend business code.
- Do not modify YOLO training/inference logic.
- Do not modify `Dockerfile` files.
- Do not modify `docker-compose.yml`.
- Do not modify current `detection_result.v1` implementation.
- Do not modify, replace, submit, or delete model weights.
- Do not change model categories/classes.
- Do not train models.
- Do not implement or test video detection.
- Do not implement or test realtime/camera detection.
- Do not implement or test Word export.
- Do not implement or test dashboard/large-screen work.
- Do not commit from this Batch4 planning step.

## 7. Batch4 Closeout Criteria for Planning Only

Batch4 Docs/Test Planning can be considered complete when:

- this file exists under `agent_outputs/docs/`;
- it clearly states Batch4 is planning only;
- future evaluation and performance checklists are defined as planned checks;
- evidence-level wording prevents planned items from being reported as completed facts;
- Batch5+ prerequisites are explicit;
- forbidden scope is preserved;
- git diff shows documentation-only changes;
- no commit has been made.

## 8. Current Planning Statement

Phase 2B Batch4 is currently **Planning Only**. This document defines future evaluation/performance acceptance shape and gate language. It does not authorize or perform implementation. Any future implementation, testing run, model evaluation, performance measurement, or feature expansion requires separate explicit authorization.

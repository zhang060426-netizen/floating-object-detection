# Phase 2B Batch3 Docker Smoke Plan

Status: WAITING FOR FULL COMPOSE SMOKE
Date: 2026-05-18
Owner: Docs/Test Agent
Scope: Smoke plan for Docker compose packaging evidence only.

## 0. Objective

Prove that the minimal Phase 2B Batch3 Docker packaging can run the currently approved scope:
- backend service;
- frontend service on `8080:80`;
- runtime model volume containing `runtime/models/yolo26n.pt` mounted to `/app/runtime/models/yolo26n.pt`;
- minimal login/model/image-detection/record-save path as applicable to the rebuilt Batch3 baseline.

This plan does **not** declare Batch3 PASS. Current state remains **WAITING FOR FULL COMPOSE SMOKE**.

## 1. Non-goals and Safety Gates

Do not include in Batch3 Docker smoke:
- video detection;
- realtime/camera detection;
- Word report export;
- dashboard or large-screen polishing;
- model training;
- model weight replacement;
- class/category changes;
- `.omx/*` artifacts as deliverables.

If any non-goal is required to make the smoke pass, stop and record a BLOCKED gate instead of expanding scope silently.

## 2. Preconditions

| Precondition | Expected state | Current evidence |
|---|---|---|
| Docker daemon | Running | MISSING / was unavailable for backend build-run attempt |
| Final compose file | Includes backend and frontend services | PARTIAL evidence: backend and frontend compose config reported PASS |
| Backend Docker artifacts | Present | REPORTED CREATED |
| Frontend Docker artifacts | Present | REPORTED CREATED |
| Runtime model file | Host `runtime/models/yolo26n.pt` exists | AI readiness says required placement; actual compose visibility pending |
| Scope guard | No business-code/weight/video/realtime/Word/dashboard expansion by Docs/Test | PASS |

## 3. Smoke Sequence

Run smoke in this order so failures remain attributable.

### Step 1 - Static compose validation

Required evidence:
- final `docker compose config` exits 0;
- rendered config includes backend service;
- rendered config includes frontend service;
- rendered config includes runtime model volume/path mapping required by AI readiness.

Gate result:
- PASS only if all three service/volume requirements are visible.
- If volume is missing, mark runtime-placement gate FAIL/BLOCKED depending on cause.

### Step 2 - Backend Docker build

Required evidence:
- backend image builds successfully from `Dockerfile.backend`;
- build uses expected `.dockerignore` context exclusions;
- no model weight is copied or modified as part of build unless explicitly approved by runtime placement contract.

Current status: **PENDING** because Docker daemon was not running during the reported attempt.

### Step 3 - Frontend Docker build

Required evidence:
- frontend image builds successfully from `Dockerfile.frontend`;
- build remains consistent with reported `npm build PASS`;
- nginx template exists and runtime env behavior is documented.

Current status: **PASS** from Frontend Agent evidence.

### Step 4 - Full compose up

Required evidence:
- `docker compose up` starts backend and frontend together;
- backend container does not crash or enter restart loop;
- frontend container serves on host `8080:80`;
- compose uses the runtime model volume rather than modifying weights.

Current status: **PENDING**.

### Step 5 - Runtime volume verification

Required evidence:
- inside backend container, `/app/runtime/models/yolo26n.pt` exists;
- file size/hash is recorded when safe and non-destructive;
- no replacement/training/class mutation occurs.

Current status: **PENDING ACTUAL COMPOSE VERIFICATION**.

### Step 6 - Backend API smoke in container

Minimum required evidence:
- backend health endpoint responds;
- auth/login or equivalent minimal auth path responds if enabled;
- model/runtime status endpoint sees the runtime model;
- image detection endpoint returns success for the approved test image;
- response envelope remains backward compatible;
- `detection_result.v1` remains preserved if the endpoint returns detection result details.

Current status: **PENDING**.

### Step 7 - Persistence / record smoke

Required when Batch3 backend record-save path is present:
- detection result is saved;
- record detail can be read back;
- generated result image/file URL is retrievable if applicable.

Current status: **PENDING**.

### Step 8 - Frontend integration smoke

Required evidence:
- open frontend via `http://localhost:8080` or equivalent host target;
- frontend loads without nginx/container errors;
- frontend configuration points to compose backend API;
- login/image-detection display path works against container backend;
- no video/realtime/Word/dashboard paths are used for the gate.

Current status: **PENDING for full integration**; isolated frontend container up/down is already PASS.

### Step 9 - Compose down cleanup

Required evidence:
- `docker compose down` completes;
- no unexpected generated files or weight changes are left behind;
- no `.omx/*` changes are included in deliverables.

Current status: **PENDING**.

## 4. PASS Criteria

Batch3 Docker smoke may be marked PASS only when all are true:

1. backend Docker build PASS;
2. backend container run/health PASS;
3. frontend Docker build/run PASS;
4. full compose backend+frontend up/down PASS;
5. runtime volume path `runtime/models/yolo26n.pt` -> `/app/runtime/models/yolo26n.pt` verified;
6. minimal backend+frontend E2E path passes through compose;
7. model weights/classes are unchanged;
8. no video/realtime/Word/dashboard scope entered;
9. evidence is recorded in `agent_outputs/docs/PHASE2B_BATCH3_DOCKER_EVIDENCE_TRACKING.md` or a successor closeout artifact.

## 5. Current Gate Result

```text
Current Docker Smoke Plan Status: WAITING FOR FULL COMPOSE SMOKE
Batch3 PASS: NOT DECLARED
Backend build/run: PENDING - Docker daemon unavailable in prior attempt
Frontend Docker build/run: PASS
AI readiness: PASS - runtime placement pending actual compose verification
Final E2E compose smoke: REQUIRED / MISSING
```

## 6. Rollback Method

If smoke fails:
- stop compose with `docker compose down` or equivalent non-destructive cleanup;
- remove only generated containers/images if explicitly part of the smoke cleanup procedure;
- do not delete model weights;
- do not edit business code from Docs/Test;
- record failing command, exit code, and logs in the evidence tracking file;
- keep Batch3 gate as WAITING/FAILED/BLOCKED rather than forcing PASS.

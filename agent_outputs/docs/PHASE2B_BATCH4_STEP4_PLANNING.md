# Phase 2B Batch4 Step 4 Planning / Gate

Status: PLANNING ONLY
Date: 2026-05-21
Phase: Phase 2B Batch4 Step 4
Current master HEAD: `7f3ef82`
Latest stable baseline: `phase2b-batch4-step3-detection-records-stable`
Latest stable baseline target: `bfe3dc9298cdcb0cb405b4189b6db151d2fea1c6`
Step 3 status: CLOSED / VERIFIED / TAGGED / ARCHIVED
Step 4 Implementation: NOT AUTHORIZED
Step 4 stable tag: NOT CREATED
Push: NOT DONE

## 1. Current Stable Baseline

The current restore baseline is:

```text
latest stable baseline: phase2b-batch4-step3-detection-records-stable
stable commit: bfe3dc9298cdcb0cb405b4189b6db151d2fea1c6
current master HEAD: 7f3ef82
Step 3: CLOSED / VERIFIED / TAGGED / ARCHIVED
Step 4: NOT AUTHORIZED
push: NOT DONE
```

Step 3 completed the detection-records list management enhancement. The current safe product chain is:

```text
login -> image detection -> save record -> records list -> record detail
```

Step 4 planning should continue this chain and avoid starting Dashboard, Word, video, realtime, backend, DB, Docker, runtime/storage, or model/training work by default.

## 2. Step 4 Candidate Direction Comparison

| Candidate | Description | Fit with current chain | Risk | Verification cost | Rollback safety | Recommendation |
|---|---|---:|---:|---:|---:|---|
| Detection record detail page enhancement | Improve detail page readability around existing record metadata, images, summary, detections, timing, and safe missing-data states. | High | Low | Low | High | Recommended |
| Detection result visualization enhancement | Improve table/visual display of detection objects and confidence/bbox presentation. | Medium-High | Medium | Medium | Medium | Possible later after detail page baseline improves |
| Detection result summary display enhancement | Add clearer summary cards/status explanations for existing detection data. | High | Low-Medium | Low-Medium | High | Good subset of recommended detail-page work |
| User experience / error prompt enhancement | Improve error copy and empty/loading states across detection flow. | Medium | Low-Medium | Medium | High | Good later cross-page polish, but broader file surface |
| Dashboard pre-planning | Plan future dashboard/large-screen metrics without implementation. | Low for current chain | Low if docs-only; high if UI starts | Low for docs | High | Planning only, not Step 4 implementation |
| Word report pre-planning | Plan future report export flow without implementation. | Low for current chain | Medium-High | Medium | Medium | Planning only, not Step 4 implementation |
| Model management pre-planning | Plan future model lifecycle UI/process improvements. | Low-Medium | Medium | Medium | Medium | Defer; separate module boundary |

## 3. Recommended Step 4 Direction

Recommended Step 4:

```text
Phase 2B Batch4 Step 4 - Detection Record Detail Readability Enhancement
```

Recommended objective:

```text
Improve the detection record detail page's readability and compatibility using only existing record data, without changing backend contracts or detection_result.v1 semantics.
```

This is the smallest safe continuation after Step 3 because Step 3 improved the records list and preserved detail navigation. Step 4 can improve what the user sees after entering a record detail, while keeping the same stable chain and a narrow frontend-only implementation surface if later authorized.

## 4. Recommendation Rationale

The detail page is the next low-risk link in the current flow:

1. Step 1 added backend timing metadata.
2. Step 2 displayed timing metadata in frontend result/detail surfaces.
3. Step 3 improved records-list management and pagination.
4. Step 4 can now make the selected record detail easier to inspect.

Reasons this is preferred:

- It continues the current product chain instead of opening a new product area.
- It can remain frontend-only by default.
- It does not need DB schema changes, backend API changes, Docker changes, storage changes, or model changes.
- It can reuse existing compatibility helpers such as record time, model display, status, target count, image refs, timing display, and backend reason display.
- It is easy to verify with build, record-detail smoke, legacy/missing data checks, and scope guard.
- It is easy to roll back as a small frontend-only diff if implementation is later authorized.

## 5. Recommended Allowed Scope for Future GO Decision

If and only if a later Step 4 Implementation GO Decision is created, the recommended file scope should be narrow and frontend-only:

Primary candidate files:

- `web-vue/src/views/DetectionRecordDetail.vue`
- `web-vue/src/components/DetectionResultPanel.vue`
- `web-vue/src/utils/detectionDisplay.ts`
- `web-vue/src/types/detection.ts`

Optional only if needed for formatting reuse:

- `web-vue/src/utils/format.ts`

Recommended implementation content, if later authorized:

- improve record detail metadata layout using existing fields only;
- make summary/count/status/model/timing sections easier to scan;
- keep original/result image display behavior unchanged or only presentation-level improved;
- keep detections table readable when objects exist;
- provide safe empty/missing-state text when detections, timing, image refs, or `detection_result` are absent;
- preserve raw `detection_result` JSON visibility if it already exists;
- preserve existing detail route and list-to-detail navigation compatibility;
- preserve `detection_result.v1` semantics exactly.

This planning document does not authorize these changes.

## 6. Explicit Forbidden Scope

Step 4 planning and any future default Step 4 implementation must not include:

- business-code changes during this planning task;
- `web-vue/**` changes during this planning task;
- `web-flask/**` changes;
- backend implementation by default;
- API response shape changes;
- DB schema changes;
- Dockerfile changes;
- `docker-compose.yml` changes;
- `runtime/**` changes;
- `storage/**` changes;
- model weight changes;
- model class/category changes;
- model training changes;
- `detection_result.v1` semantic changes;
- Dashboard / large-screen implementation;
- Word report implementation;
- video detection implementation;
- realtime detection implementation;
- delete records;
- bulk delete records;
- edit records;
- auth/login semantic changes;
- upload flow semantic changes;
- image detection main-flow semantic changes;
- push;
- tag creation.

## 7. Recommended Agent Division

| Agent | Recommended Step 4 responsibility |
|---|---|
| Frontend Agent | Future implementation owner only after a separate GO Decision; keep work limited to record-detail readability and compatibility. |
| Backend Agent | Read-only contract check only; confirm existing record detail API is sufficient and no backend change is required by default. |
| Docs/Test Agent | Own Step 4 verification checklist, evidence archive, scope guard, and closeout docs if implementation is later authorized. |
| AI Agent | No Step 4 implementation role; no model, training, class, weight, inference-chain, video, or realtime work. |

Recommended default decision:

```text
Frontend implementation: NOT AUTHORIZED YET
Backend implementation: NOT AUTHORIZED
Backend read-only verification: allowed only after a Step 4 GO Decision requests it
Docs/Test checklist: allowed only as documentation planning/checklist work
AI implementation: NOT AUTHORIZED
```

## 8. Verification Requirements for a Future Authorized Step 4

Future Step 4 implementation should be accepted only after evidence covers:

1. Build / static checks:
   - `npm.cmd run build` or `npm run build` from `web-vue/`;
   - `git diff --check`.
2. Record detail smoke:
   - navigate from records list to record detail;
   - detail page loads;
   - existing images/metadata/detections/JSON sections remain available where data exists;
   - no regression in the back/list navigation path if present.
3. Compatibility smoke:
   - missing `detection_result` does not crash;
   - missing detections array does not crash;
   - missing timing does not crash;
   - legacy `detection_result.timing_ms` remains compatible where timing display is used;
   - missing original/result image refs use safe empty/fallback behavior;
   - legacy/no-timing records remain compatible.
4. Scope guard:
   - only future-authorized frontend files changed;
   - no `web-flask/**` changes;
   - no Docker, DB, runtime/storage, model/weight/category/training changes;
   - no Dashboard, Word, video, realtime, delete/bulk-delete/edit-record features;
   - `detection_result.v1` semantics preserved.
5. Regression checks:
   - login path still works if smoke environment is running;
   - image detection path is not semantically changed;
   - records list still displays and detail jump still works.

## 9. Rollback Baseline

Rollback baseline for any future Step 4 implementation should be the current planning start point:

```text
rollback baseline commit: 7f3ef82
rollback baseline meaning: Step 3 archived on master; Step 4 implementation not started
latest stable baseline: phase2b-batch4-step3-detection-records-stable
latest stable baseline target: bfe3dc9298cdcb0cb405b4189b6db151d2fea1c6
```

If Step 4 is later implemented and must be reverted:

- revert only Step 4 implementation commits and Step 4 verification/closeout docs;
- do not alter the Step 3 stable tag unless separately authorized;
- no backend rollback should be needed under the recommended default scope;
- no DB, Docker, runtime/storage, model, weight, class, or training rollback should be needed.

## 10. GO Decision Requirements Before Implementation

Before any Step 4 implementation begins, create a separate GO Decision document that restates:

- exact Step 4 name;
- exact authorized agent(s);
- exact authorized file paths;
- backend read-only or implementation decision;
- implementation content allowed;
- forbidden scope;
- verification commands and smoke checklist;
- rollback baseline;
- push status;
- stable tag status.

Planning does not equal implementation authorization.

## 11. Current Decision

```text
Phase 2B Batch4 Step 4 Planning: OPENED
Recommended Step 4: Phase 2B Batch4 Step 4 - Detection Record Detail Readability Enhancement
Step 4 Implementation: NOT AUTHORIZED
Step 4 stable tag: NOT CREATED
push: NOT DONE
business code changes: NOT DONE
web-vue changes: NOT DONE
web-flask changes: NOT DONE
Docker changes: NOT DONE
DB schema changes: NOT DONE
runtime/storage changes: NOT DONE
model/weights/classes/training changes: NOT DONE
Dashboard / Word / video / realtime implementation: NOT DONE
```

## Phase 2B Batch4 Step 4 Post-Tag Archive

```text
Step 4 stable tag: phase2b-batch4-step4-detail-readability-stable
tag commit: 66349abc9ba3f8ad4a31afe85d5430a52b0a4393
master HEAD before archive: 66349ab
Step 4 status: CLOSED / VERIFIED / TAGGED
push: NOT DONE
Step 5: NOT AUTHORIZED
```

Implementation summary:

- Detection record detail page readability enhancement.
- Fixed timing Chinese label garbling.
- Added file name display.
- Added detection status `el-tag`.
- Displayed timing information as an independent section.
- Compatible with missing `detection_result`, missing timing, legacy `timing_ms`, empty detections, and old records.
- Preserved JSON collapse, image display, API contract, and `detection_result.v1` semantics.

This is a documentation-only post-tag archive. It records the already-created Step 4 stable tag and does not push, create a new tag, edit business code, or authorize Step 5 implementation.

# Task: Phase 2B Batch2 Docs/Test Planning

Status: PLANNING ARTIFACT ONLY
Owner: Docs/Test Agent
Phase: Phase 2B Batch2
Date: 2026-05-17

## 1. Boundary

Batch2 planning artifact creation is allowed. Batch2 implementation is not started by this file.

Allowed scope:
- Create task files, smoke test plan, gate checklist, and acceptance template.
- Record Batch1 FULL PASS CANDIDATE as the starting point.
- Define evidence requirements for Batch2 without changing business code.
- Keep append-only traceability for smoke evidence.

Forbidden scope:
- Do not modify frontend/backend/AI business code.
- Do not modify model weights.
- Do not expand Batch2 to video, realtime, Word report, dashboard, or large-screen features.
- Do not authorize Batch2 implementation.

## 2. Docs/Test Batch2 Planning Objectives

1. Provide per-agent planning tasks.
2. Provide Batch2 smoke test plan.
3. Provide Batch2 gate checklist.
4. Provide Batch2 acceptance template.
5. Maintain compatibility requirement: `detection_result.v1` must remain backward compatible.

## 3. Acceptance Targets

| Artifact | Required result |
|---|---|
| `tasks/backend/TASK_PHASE2B_BATCH2.md` | Backend planning task exists |
| `tasks/frontend/TASK_PHASE2B_BATCH2.md` | Frontend planning task exists |
| `tasks/ai/TASK_PHASE2B_BATCH2.md` | AI planning task exists |
| `tasks/docs/TASK_PHASE2B_BATCH2.md` | Docs/Test planning task exists |
| `agent_outputs/docs/PHASE2B_BATCH2_SMOKE_TEST_PLAN.md` | Smoke plan exists |
| `agent_outputs/docs/PHASE2B_BATCH2_GATE_CHECKLIST.md` | Gate checklist exists |
| `agent_outputs/docs/PHASE2B_BATCH2_ACCEPTANCE_TEMPLATE.md` | Acceptance template exists |

## 4. Handoff Notes

- After creation, report file list and uncommitted status.
- Do not commit `.omx/*`.
- Any future implementation requires explicit Leader authorization.

---

## 5. Stage1 Docs/Test Update - 2026-05-17

Status: Stage1 smoke tracking active; waiting for evidence.

Created Stage1 artifacts:
- `tasks/docs/TASK_PHASE2B_BATCH2_STAGE1.md`
- `agent_outputs/docs/PHASE2B_BATCH2_STAGE1_SMOKE_EVIDENCE_TEMPLATE.md`
- `agent_outputs/docs/PHASE2B_BATCH2_STAGE1_SMOKE_TRACKING_REPORT.md`

Updated:
- `agent_outputs/docs/PHASE2B_BATCH2_GATE_CHECKLIST.md`

Required evidence slots now tracked:
- backend pytest;
- frontend build;
- runtime diagnostics;
- image detection response;
- result image URL;
- records detail.

Scope remains docs/test tracking only. No business code, weight, video, realtime, Word, dashboard, or large-screen work is authorized by this update.

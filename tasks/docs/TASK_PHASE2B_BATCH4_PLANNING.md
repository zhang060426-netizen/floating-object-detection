# TASK_PHASE2B_BATCH4_PLANNING — Docs/Test Agent

Status: PLANNING ONLY
Owner: Docs/Test Agent
Phase: Phase 2B Batch4
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`

## 1. Context

Phase 2B Batch3 is closed, archived, tagged, and final-smoke verified. Batch4 may only create planning artifacts. Docs/Test owns the planning gate and evidence boundaries.

## 2. Allowed Scope

- Create and maintain Batch4 planning gate documentation.
- Define evaluation-resource and performance-test planning checklists.
- Track AI/Backend/Frontend planning outputs.
- Ensure all evidence levels distinguish historical metrics, runtime smoke, and future planned evaluation.
- Preserve the rule that Batch4 implementation is not authorized.

## 3. Forbidden Scope

- Do not modify business code.
- Do not modify Dockerfile or docker-compose.yml.
- Do not modify `detection_result.v1`.
- Do not modify model classes or weights.
- Do not run training, validation, or full model evaluation.
- Do not enter video, realtime, Word, dashboard, or large-screen scope.
- Do not start Batch4 implementation.

## 4. Planning Deliverables

Recommended Docs/Test planning outputs:

- `agent_outputs/docs/PHASE2B_BATCH4_MASTER_PLANNING_GATE.md`
- `agent_outputs/docs/PHASE2B_BATCH4_EVALUATION_TEST_PLAN.md` optionally later

This task creates the master planning gate. Additional docs require explicit planning continuation.

## 5. Required Questions to Answer

1. Are all Batch4 tasks planning-only?
2. Are all forbidden scopes explicitly preserved?
3. Are evidence levels clear for current runtime smoke vs historical metrics?
4. Which documents must exist before any future implementation proposal?
5. What is the default decision on entering implementation?

## 6. Acceptance Criteria

- Master planning gate exists.
- Four Agent task boundaries are recorded.
- Batch4 implementation remains blocked by default.
- No business code, Docker config, model, class, weight, or schema files are changed.
- Next step is planning review, not implementation.

## 7. Handoff Notes

Docs/Test should not mark Batch4 implementation as ready. The only allowed next state is Batch4 planning review unless the project owner explicitly authorizes a separate implementation gate later.

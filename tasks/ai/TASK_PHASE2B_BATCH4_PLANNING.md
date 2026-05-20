# TASK_PHASE2B_BATCH4_PLANNING — AI Agent

Status: PLANNING ONLY
Owner: AI Agent
Phase: Phase 2B Batch4
Baseline tag: `phase2b-batch3-docker-compose-stable`
Baseline code point: `fddb0c8`
Archive commit: `ff731de`

## 1. Context

Phase 2B Batch3 is closed and archived. Docker Compose final smoke passed with `detection_result.v1` preserved and runtime model mount confirmed.

Batch4 is **planning only**. The AI lane focuses on model quality, current YOLO26n baseline limitations, future evaluation design, and future model upgrade criteria.

## 2. Allowed Scope

- Plan current YOLO26n baseline quality analysis.
- Separate runtime-chain smoke success from model-accuracy claims.
- Review existing model asset evidence and historical metrics at documentation level.
- Plan future evaluation methodology using existing image/label resources.
- Plan criteria for future higher-precision model introduction.
- Plan ONNX / TensorRT feasibility as future work only.
- Preserve `class_id=0` and `class_name=floating_object`.
- Preserve `detection_result.v1` compatibility.

## 3. Forbidden Scope

- Do not train.
- Do not run validation or full benchmark jobs.
- Do not export ONNX.
- Do not create TensorRT engines.
- Do not replace, move, delete, or commit model weights.
- Do not modify model class/category definitions.
- Do not edit Flask/Vue/YOLO business code.
- Do not modify Dockerfile or docker-compose.yml.
- Do not enter video, realtime, Word, dashboard, or large-screen scope.
- Do not start Batch4 implementation.

## 4. Planning Deliverables

Recommended AI planning outputs:

- `agent_outputs/ai/PHASE2B_BATCH4_MODEL_QUALITY_PLAN.md`
- `agent_outputs/ai/PHASE2B_BATCH4_MODEL_UPGRADE_ROADMAP.md`

These deliverables should remain planning artifacts only.

## 5. Required Questions to Answer

1. What evidence proves the current mounted model is `yolo26n.pt` dev baseline?
2. Which historical metrics are only historical-output evidence and not current runtime proof?
3. What minimal future evaluation dataset and labels should be used?
4. What metrics should future model-quality evaluation collect?
5. What evidence would be required before replacing the runtime model?
6. What would ONNX / TensorRT require later, without implementing it now?

## 6. Acceptance Criteria

- Current YOLO26n baseline limitations are documented.
- Historical metrics are clearly separated from current runtime smoke.
- Future evaluation method is defined without running evaluation.
- Future model upgrade criteria are defined.
- ONNX/TensorRT are documented only as future feasibility topics.
- No weights, classes, training scripts, runtime code, or Docker files are changed.

## 7. Handoff Notes

Backend may use AI planning outputs to plan performance metrics and additive metadata. Frontend may use them to plan model-quality notices. Docs/Test owns final Batch4 planning gate aggregation.

# Phase 2B Batch4 Step 7 Record Filter Verification Checklist Draft

Status: SUPERSEDED BY FORMAL EVIDENCE / RETAINED PLANNING DRAFT
Date: 2026-05-23
Owner: Docs/Test Agent
Phase: Phase 2B Batch4 Step 7
Step 7 scope: Detection Records Filter/Search Enhancement
Master HEAD: `1d81d33`
Step 7 Planning commit: `c40e016`
Latest stable tag: `phase2b-batch4-step6-dashboard-stable` -> `708a61a`
Push: **NOT DONE**
Step 7 stable tag: **NOT CREATED**

## Supersession Notice

This planning-only draft is retained as the pre-implementation verification checklist input. Step 7 was subsequently authorized, implemented, merged, and verified. The authoritative Step 7 closeout records are:

```text
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_VERIFICATION_EVIDENCE.md
agent_outputs/docs/PHASE2B_BATCH4_STEP7_RECORD_FILTER_CLOSEOUT.md
```

Formal closeout state:

```text
Step 7 scope: Detection Records Filter/Search Enhancement
master HEAD before docs closeout: 224e12d
Backend merge commit: 35d4950
Frontend merge commit: 224e12d
GO Decision merge commit: aef6c18
Planning merge commit: 1d81d33
latest previous stable tag: phase2b-batch4-step6-dashboard-stable -> 708a61a
Step 7 stable tag: NOT CREATED
recommended stable tag: phase2b-batch4-step7-record-filter-stable
recommended tag target: 224e12d
push: NOT DONE
Step 8: NOT AUTHORIZED
```

The checklist below records the original planning-gate expectations and is no longer the authoritative verification result.

## 0. Purpose and Gate Boundary

This draft prepares the future verification checklist for a separately authorized Step 7 implementation of detection-record filtering and search.

This document is a docs/test planning artifact only. It neither implements nor authorizes edits to frontend or backend business code, database contracts, runtime/deployment configuration, storage, or model/inference behavior.

```text
Step 7 Implementation: NOT AUTHORIZED
GO Decision required before any business-code implementation: YES
```

## 1. Step 7 Scope

Proposed Step 7 enhancement:

```text
Detection Records Filter/Search Enhancement
```

Expected intent, subject to a future explicit GO Decision:

- add narrow, optional filtering/search behavior to the existing detection-record list flow;
- preserve the existing login -> image detection -> save record -> records list -> detail -> Word report -> Dashboard chain;
- preserve current authorization boundaries, pagination compatibility, existing record compatibility, and `detection_result.v1` semantics;
- remain additive and reversible, with no database schema change by default.

## 2. Backend Expected Checklist

Future authorized backend implementation evidence should verify:

- [ ] `GET /api/detection/records` continues to require and honor JWT authentication.
- [ ] Existing `page` / `page_size` pagination parameters continue to work without filters.
- [ ] Existing `page` / `page_size` pagination parameters continue to work when filters are applied.
- [ ] Optional `keyword` / filename search is supported according to the later approved API query contract.
- [ ] Optional `model_id` filter is supported according to the later approved API query contract.
- [ ] Optional `detection_status` filter is supported according to the later approved API query contract.
- [ ] Optional date range filter is supported only if specifically included in the final GO authorization.
- [ ] Admin users can see/filter all authorized detection records under the existing permission model.
- [ ] Normal users can see/filter only their own detection records.
- [ ] No DB schema change, migration, SQL initialization change, or storage-layout change is introduced.
- [ ] Records with missing or malformed `detection_result` remain safely readable/listable.
- [ ] No semantic change is made to `detection_result.v1`.

Backend compatibility checks to retain:

- [ ] Omitting all optional filter parameters preserves the existing list behavior.
- [ ] Empty/no-match filtered results return a safe empty list response compatible with the frontend.
- [ ] Filter composition does not bypass JWT or user/admin record visibility enforcement.

## 3. Frontend Expected Checklist

Future authorized frontend implementation evidence should verify:

- [ ] `DetectionRecords.vue` gains a narrow filter/search bar without redesigning unrelated record-page behavior.
- [ ] A keyword input is present for filename/keyword search.
- [ ] A status select control is present.
- [ ] A model input or select control is present.
- [ ] A date range picker is present only if specifically included in the final GO authorization.
- [ ] A search button submits the current filter state.
- [ ] A reset button clears filter state and restores the default records list.
- [ ] Pagination remains linked to active filters and correctly reloads filtered pages.
- [ ] Existing record-detail jump/navigation remains available and functional.
- [ ] Existing refresh behavior remains available and functional.
- [ ] Existing empty-state behavior remains safe and understandable, including no-match filtered results.

Frontend compatibility checks to retain:

- [ ] Filters are additive to the existing records list rather than a new workflow.
- [ ] Applying or resetting filters has an explicitly verified page-state behavior, expected to return safely to the first page when criteria change.
- [ ] Detail, Word report entry, and Dashboard navigation are not semantically changed by the records-list enhancement.

## 4. Verification Commands

The following commands are proposed for later use after Step 7 implementation is separately authorized and implemented.

### Backend

```powershell
cd web-flask
python -m compileall .
python -m pytest
```

### Frontend

```powershell
cd web-vue
npm.cmd run build
```

### General

```powershell
git diff --check
git status --short --branch
```

General pass criteria:

- [ ] `git diff --check` reports no whitespace errors.
- [ ] The implementation verification worktree is clean after its authorized commit/verification process, or any expected evidence-only files are explicitly recorded.

## 5. Manual Verification Checklist

After a separate Step 7 GO Decision and authorized implementation, manually verify:

- [ ] With no filters selected, the default detection-record list loads normally.
- [ ] Keyword search returns the expected filename/keyword-matching records.
- [ ] Status filter returns records matching the selected detection status.
- [ ] Model filter returns records matching the selected model.
- [ ] Date range filter returns records inside the selected range, only if that filter is authorized in the final GO Decision.
- [ ] Pagination works correctly after one or more filters are applied.
- [ ] Reset clears active filters and restores the default list behavior.
- [ ] A normal user can view/filter only that user's own records.
- [ ] An administrator can view/filter all records allowed under existing admin behavior.
- [ ] Dashboard behavior and reachability are unaffected.
- [ ] Detection record Detail behavior and reachability are unaffected.
- [ ] Word report behavior and reachability are unaffected.

Suggested compatibility/manual edge cases:

- [ ] A filtered request returning no records renders the existing empty state without crash.
- [ ] Records missing `detection_result`, containing `null` detection results, or containing malformed optional result content do not break list rendering or detail navigation.
- [ ] Existing unfiltered callers do not need to send new parameters.

## 6. Explicit NO-GO

The following are expressly prohibited until separately authorized, and remain out of scope for this draft:

- [ ] No Step 7 implementation before a GO Decision.
- [ ] No video or realtime detection enhancement.
- [ ] No AI Agent / LLM feature.
- [ ] No DB schema change unless explicitly authorized by a later decision; default is **NO-GO**.
- [ ] No Docker, runtime, or storage change.
- [ ] No model, weights, classes, or training change.
- [ ] No `detection_result.v1` semantic change.
- [ ] No push.
- [ ] No tag.

## 7. Docs/Test Draft Completion Assertion

For this draft-preparation task only:

```text
Checklist draft prepared: YES
Step 7 scope documented: Detection Records Filter/Search Enhancement
Business code changed: NO
web-vue/** changed: NO
web-flask/** changed: NO
DB / Docker / runtime / storage changed: NO
Model / weights / classes / training changed: NO
Step 7 implementation performed: NO
Step 7 Implementation: NOT AUTHORIZED
Commit performed for this task: NO
Push performed: NO
Tag created: NO
```

## 8. Future Verification Evidence Record Template

Complete only after a later explicit GO Decision authorizes Step 7 implementation:

```text
GO Decision commit:
Authorized implementation file scope:
Backend verification result:
Frontend build result:
Manual verification result:
Permission-boundary verification result:
Compatibility verification result:
git diff --check result:
Rollback reference: phase2b-batch4-step6-dashboard-stable -> 708a61a
Remaining risks:
```

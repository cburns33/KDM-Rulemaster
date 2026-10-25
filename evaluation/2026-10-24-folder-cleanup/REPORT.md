# Folder cleanup, 24 October 2026

## Result

Consolidated the objective, phases, and next steps without changing app answer behavior or adding coverage. [The root README](../../README.md) is the starting point. [The roadmap](../../docs/OBJECTIVE_AND_ROADMAP.md) owns direction and phase checkpoints; [status](../../docs/STATUS.md) is the single current handoff. The planning target remains the group's 1.5 core game; the exact first-release coverage checklist is the next planning task, not a claim of complete existing support.

All work was confined to `D:\Documents\KDM\KDM-Rulemaster-v2` on `rules-v2`. The separate `main` checkout was not opened internally or changed. Existing uncommitted card-coverage changes were preserved. No commit, push, deployment, credential change, or external data request was performed.

## Consolidated navigation

- [Objective and roadmap](../../docs/OBJECTIVE_AND_ROADMAP.md): project evolution, current objective, release direction, six phases, and next work.
- [Current status](../../docs/STATUS.md): current capabilities, limits, verification, and immediate actions.
- [Coverage](../../docs/COVERAGE.md): all current reviewed topics, mapped source pages, and card-image evidence, generated from current records. Each local source link was checked for existence before writing.
- [Sources](../../docs/SOURCES.md): review workflow, provenance boundaries, source locations, Git versus local-only preservation, and regeneration.
- [App guide](../../kdm-assistant/README.md): launch, optional Sol configuration, behavior limits, checks, and future hosting procedure. Corrected key paths and optional source-manifest descriptions.
- [Evaluation index](../INDEX.md): separates current development/source evidence, historical answer audits, dormant method experiments, and organization work.

Mutable next actions no longer live in `AGENTS.md`. It links to current guidance and retains working boundaries. The next sequence is scope/coverage checklist, fresh end-to-end evaluation, repair of material process failures, and then prioritized coverage acquisition. Cunning remains unverified and outside active work.

## Archived and grouped material

Thirteen named files were moved within the worktree. Every move checked source/target containment and preserved the file length. Original and focused PDF contents were not read or modified.

- Prior root status and iteration guide moved to `docs/history/handoffs/` as dated snapshots.
- The previous app guide was copied there before its live version was rewritten, preserving detailed old instructions and project comparisons.
- Four OCR/catalog documents moved to `docs/history/research/ocr/` with a paused-track index.
- Wiki commands and historical context were preserved under `docs/history/research/wiki/`. Experiment modules, tests, and ignored drafts remain in their original locations to preserve imports and commands.
- Two old UI previews moved to `docs/history/design/`.
- The player introduction moved to `docs/player/` without a rules rewrite.
- Community scenarios moved to `evaluation/community/` and are indexed as development/regression material.
- Original PDF, focused PDF, and page map moved together to `sources/` with original filenames.

The [history index and relocation map](../../docs/history/README.md) explains old filenames and stale instructions. The archived iteration guide's relative evaluation hyperlink was repaired. Other historical content, raw outputs, and recorded working-tree snapshots were retained rather than rewritten as current facts.

## Dependencies and preservation

`prepare.py` now resolves the focused PDF and page map under `sources/`. That is the only existing app-code change made by this cleanup. Its legacy image lookup remains unchanged. A new rebuild test exercises the relocated map and PDF paths in an isolated workspace, mocking rendering instead of opening a large PDF.

The app, active tests, public page/card images, original local image evidence, and dated evaluation folders keep their locations. Historical harness directory depth and sibling dependencies remain intact. Both distinct PDFs are retained. Ignored original evidence and wiki artifacts remain local and are called out in the source inventory so they are not mistaken for disposable cache.

Automatic approval review rejected the initial combined move-and-delete command without a specific reason. Retrying the validated file moves without deletion succeeded. The empty `tmp/` directory was left in place. No useful source, evaluation result, or history was deleted.

## Verification

- All 101 Python tests pass, including local/hosted source citation checks and the new source-relocation rebuild check.
- The rebuild check uses the actual page map in a temporary project, verifies the new focused-PDF command path, and checks the generated mapping and renamed page outputs. It leaves live assets and manifest unchanged.
- The coverage generator resolved 25 reviewed topics across 28 unique source pages and verified every linked local image exists before writing the inventory.
- Moved files preserved their lengths. Large source files were moved without reading their contents.
- New navigation targets were checked for existence. Dated evaluation reports and raw results were not re-ingested for this task.
- `git diff --check` passes. No new live Sol call, browser evaluation, or deployment check was needed for this organization change.

The launch-identity issue remains a documented follow-up, outside this folder cleanup. The latest source-selection regression results remain development evidence, not independent answer-accuracy claims.

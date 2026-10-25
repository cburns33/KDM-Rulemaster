# Project folder audit, 24 October 2026

## Conclusion

The application folder has a workable structure. Project guidance has accumulated contradictory current-state descriptions and dormant research instructions. The main cleanup need is a clear distinction between current guidance, active app assets, historical evidence, and paused experiments.

This audit covers the active `KDM-Rulemaster-v2` worktree on `rules-v2`. The separate `main` checkout and pre-Git archive were not inspected internally or changed. Large PDFs, large card photos, raw result datasets, and credentials were not opened. File metadata, Markdown guidance, and targeted code sections were sufficient for this audit. Existing uncommitted application changes were preserved. No files were moved or deleted, and no app code was changed during this audit.

## Findings and recommended treatment

### 1. Several documents compete to describe the current project

Priority: high. Rewrite current guidance before adding more handoff sections.

- `KDM_Project_Status.md` had five sections labeled Current handoff before the archive boundary. They include successive snapshots with 25, 22, and 18 topics and different next actions. The October 7 handoff still says Maul and Combo Claw photos are unavailable. Those statements were valid historical observations and are superseded by October 24 photo-backed records.
- `ITERATION_2.md` opens with newer additions, but its Current scope section still describes 18 reviewed records, missing Maul and Combo Claw photos, and a next source check that includes Cunning. It ends with an 81-test baseline. The latest verified suite has 100 tests. The mission remains useful; the mixed chronology obscures it.
- `AGENTS.md`, `ITERATION_2.md`, `KDM_Project_Status.md`, and the app README duplicate coverage and next-step information. My latest handoff additions contributed to that duplication.
- The preceding conversation proposed a release-scope and coverage map followed by end-to-end evaluation. The project files still foreground another card batch. The proposed first-release scope has not been approved or written as an acceptance checklist.

Recommendation: retain one short current status, one objective/roadmap document, and one app operation guide. Move old handoff content into a dated history document during a separate cleanup pass. Keep `AGENTS.md` focused on working rules and links, with mutable project facts owned by the status document. Mark the proposed release scope as proposed until settled.

### 2. The OCR planning files describe a paused approach

Priority: medium. Preserve as research history, remove from the active navigation path.

Candidates:

- `KDM_Early_Game_Card_Shortlist.md`
- `KDM_OCR_Queue.md`
- `KDM_OCR_Benchmark_Selection.md`
- `KDM_OCR_Benchmark_Source_Audit.md`

These concern Simulator catalog paths, encrypted image extraction, deduplication, and a provisional 24-card method benchmark. They do not describe the current rulebook-face and physical-photo workflow. The queue still lists Ground Fighting and Founding Stone as acquisition candidates even though their rulebook faces now support app records. The catalog facts and OCR failure examples remain useful historical evidence; they should not be treated as the current coverage checklist.

Recommendation: label the track paused and group these documents under research history. Maintain a new source/coverage inventory for current intake. Do not restart OCR solely because an old queue contains entries.

### 3. Wiki tooling is an isolated experiment, while the README gives it prominence

Priority: medium. Mark dormant and separate its operating instructions.

`wiki_stage.py`, `wiki_extract.py`, and `wiki_preview.py` are standalone intake/preview tools. The local and hosted answer paths do not import them. Their corresponding `test_wiki_*.py` files still test those tools and are valid tests for the retained experiment.

The README's Source handling section leads with commands for staging and previewing wiki drafts. That presentation can make the experiment look like the main ingestion process. The current reviewed card records use physical photos or rulebook images. Existing wiki drafts remain unreviewed and outside runtime retrieval.

Recommendation: preserve tools, tests, drafts, and provenance as a dormant experiment; move their detailed instructions out of the main app guide. A later physical relocation needs import and path changes. Do not delete the tests while retaining the tooling.

### 4. The app README contains concrete stale operational details

Priority: high. Correct these when consolidating documentation.

| Location | Observed mismatch | Correction needed |
| --- | --- | --- |
| README, Optional Sol explanations | Names `D:\Documents\KDM\.env` as the key location. `sol_answer.py` checks the worktree-root `.env`, then the app-folder `.env`, then environment variables. | Document the paths that the code uses. No credential contents were inspected. |
| README, Source handling | Describes `data/source-manifest.json` as an available inventory. That file is absent in this worktree. | Describe it as an optional generated artifact or regenerate it only if needed. The tracked `data/manifest.json` exists and supplies page mappings. |
| README, final paragraph | Says `prepare.py` is needed only in the original workspace. `server.init()` still calls it if the manifest is missing. | Document the active bootstrap fallback and its actual inputs. |
| README, hosting instructions | Includes deployment steps next to a branch warning that hosting is not cleared. | Present hosting as a future release procedure with a clear current branch status. No deployment verification was part of this audit. |
| README, coverage table | Lists 19 topics while the app has 25. The opening count is current. | Label the table as selected coverage or complete it from the current records. |

`prepare.py` contains a legacy `work/pdf-triage` lookup outside the worktree. That folder is absent at the resolved location. The script also has a fallback using the focused PDF and Poppler, so the missing legacy path alone does not establish a broken setup. Keep the file because it is still reachable from app startup. Its fallback was inspected, not executed.

### 5. Historical evaluations are valuable, with unclear navigation

Priority: medium. Add an index before moving anything.

At audit time, `evaluation/` contained 18 dated directories and 45 files, about 0.60 MiB. It mixes source audits, OCR trials, model-output audits, retests, and current source-selection regression checks. There is no top-level evaluation index explaining which results describe the current app or which cases became development fixtures.

Keep the historical results. They document prior errors, source provenance, and the limits of accuracy claims. The old `run.py` scripts are dated experiment harnesses, distinct from the active `kdm-assistant/test_*.py` regression suite. Some compute the app location from their directory depth, and some read sibling evaluation folders. Moving them into a deeper archive without updating paths would break reruns.

Recommendation: add an index with purpose, tested version/scope, and historical or current relevance. Preserve dated paths unless a planned move also updates dependencies. The early community questions are useful regression history, with the document's existing warning that they are not a blind benchmark.

### 6. Source files and supporting artifacts need clear homes

Priority: medium. Preserve evidence and change paths only with a dependency check.

| Item | Classification | Recommended treatment |
| --- | --- | --- |
| Original rulebook PDF and focused rulebook PDF | Distinct source and derivative, with different page counts and numbering | Keep both. They are not disposable duplicate downloads. A future move of the focused PDF must update `prepare.py`. |
| `KDM_Rules_Focused_Page_Map.md` | Active mapping and regeneration input | Keep accessible; any move must update `prepare.py`. |
| `kdm-assistant/public/pages/` | Active source images used by local and hosted app | Keep in place. |
| `kdm-assistant/public/cards/` | Active cited card evidence | Keep in place, including the older Grasp PNG, which remains referenced by server handling and tests. |
| `kdm-assistant/data/card-reference-images/` | Original and supplementary source evidence | Preserve. Copies of the physical card images in `public/cards` serve a different distribution purpose. |
| `kdm-assistant/data/wiki-candidates/` and `wiki-drafts/` | Unreviewed experimental source artifacts | Preserve and mark dormant. These directories are ignored by Git and will not accompany a fresh clone. |
| `KDM_Assistant_Preview.png` and `KDM_Assistant_Expanded_Preview.png` | Design preview artifacts with no runtime references found | Archive as design history; do not present as the current UI. Their visual layouts were not inspected in this audit. |
| `KDM_New_Player_Intro_and_Prologue_Reference.md` | Player handout, separate from app engineering | Keep under player materials. This audit does not reverify its rules text. |
| `tmp/` | Empty temporary directory | Optional housekeeping candidate. No substantive cleanup benefit. |
| `__pycache__/` | Ignored generated Python cache | Disposable, with no need to make cache removal a project task. |

The root held ten Markdown files before this report, alongside both PDFs and the design images. That mixture makes the active starting point hard to identify. There is no root README that routes a reader to current status, roadmap, source workflow, app instructions, and evaluation evidence.

The whole app `data/` directory is ignored, with the existing manifest tracked as an exception through Git history. Published physical card copies are tracked, while extra source evidence and wiki artifacts are local. A source inventory should state which files are reproducible from Git and which require local preservation. Ignored evidence should not be treated as disposable cache.

### 7. Multiple checkouts create an app-launch ambiguity

Priority: medium. Track as a launch issue to fix before group use.

`launch.py` opens any service on port 8765 whose health response identifies itself as `lantern-archive`. The response does not identify this worktree. If another checkout is running the same app there, launching from `rules-v2` can open that instance. This is an inference from the launcher logic, not a reproduced runtime incident. There is no need to open or change `main` to address the active checkout's identity check in a later fix.

## Proposed organization

This is a target layout for a separate cleanup pass, not a description of moves performed by this audit.

```text
KDM-Rulemaster-v2/
  README.md                    Starting point and links
  AGENTS.md                    Working rules and scope boundaries
  docs/
    OBJECTIVE_AND_ROADMAP.md   Proposed release scope, phases, acceptance checks
    STATUS.md                 One current status and next actions
    SOURCES.md                Source workflow and inventory
    player/                   Player handout
    history/                  Previous handoffs, OCR/wiki research, design previews
  sources/                    Original and focused PDFs, with mapping references
  evaluation/
    INDEX.md                  Which audits matter and what they establish
    <existing dated folders>  Evidence retained at its current depth
  kdm-assistant/               App and active tests, kept structurally intact
```

The exact filenames matter less than giving each fact one current home. Do not move the app, page images, card images, tests, or evaluation harnesses merely to make the tree look tidy.

## Recommended next actions

1. Consolidate current objective/status guidance and label historical handoffs. Incorporate the preceding roadmap discussion as a proposal, preserving unresolved release-scope decisions.
2. Correct the app README's paths, absent-file description, incomplete coverage table label, and current versus future hosting instructions.
3. Add evaluation navigation and a source/coverage inventory. Label OCR and wiki work as paused experiments.
4. Group root research notes, preview artifacts, and player material into their intended homes, updating references as part of each move. Preserve evidence and historical results.
5. Address launch identity before relying on the app to demonstrate the active branch.

Only the audit report and required status notes were written during this audit. No tests were rerun because app behavior was unchanged. The last recorded code verification remains 100 passing Python tests from the preceding card batch.

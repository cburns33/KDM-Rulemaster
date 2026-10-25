# Evaluation index

The [current status](../docs/STATUS.md) owns present verification counts. The [roadmap](../docs/OBJECTIVE_AND_ROADMAP.md) defines the evaluation still needed before release. Dated results below describe their tested scope and version, not the accuracy of every later app version.

## Latest development and source evidence

The [early-campaign coverage and diagram repair](2026-10-24-early-campaign-coverage/REPORT.md) adds eight bounded reviewed units and brings the app to 33 topics/36 source pages. All 126 automated tests pass. The final snapshot includes 33 responses and seven live Sol answers, including two diagram cases. First and final development snapshots are separate; baseline files remain byte-preserved. Required card and procedure gaps remain open.

The [retrieval/table regression](2026-10-24-retrieval-regression/REPORT.md) follows general subject-selection, table-parsing, and context fixes. All 115 automated tests pass; the final 20 turns per mode pass targeted source/table checks, with three actual Sol calls. Missing required rules remain gaps. These are regression results, not release approval.

The [first-release baseline results](2026-10-24-release-baseline/REPORT.md) cover 32 scenarios and 36 turns per mode, with 30 actual Sol calls and no request failures. All original questions, first responses, grades, metadata, report, and harness remain unchanged. The fixes and reruns live in the separate regression directory. The baseline is source-guided development evidence, not an independent blind benchmark.

| Evaluation | Purpose and limits |
| --- | --- |
| [Next card coverage](2026-10-24-next-card-coverage/REPORT.md) | Rulebook-backed Founding Stone, Strange Hand, Clever Ploy, and Ground Fighting sources; fixed source-selection development cases. No independent accuracy estimate or live Sol evaluation. |
| [Fresh card questions](2026-10-24-fresh-card-questions/REPORT.md) | Initial fresh local questions followed by fixes and regression reruns. Maul replaced Cunning in the active fixture. |
| [White Lion promotion](2026-10-24-white-lion-promotion/REPORT.md) | Physical-photo-backed records and source-selection checks. |
| [Physical White Lion photos](2026-10-24-physical-white-lion-cards/REPORT.md) | Image/provenance review for the group's six supplied 1.5 cards. |
| [Online image comparison](2026-10-11-online-card-images/REPORT.md) | Prior image comparisons with unresolved edition/provenance limits for the data-card draft. |

## Historical answer audits and fixes

| Evaluation | Purpose |
| --- | --- |
| [September 29 audit](2026-09-29/REPORT.md) | Earlier live answer failures and missing coverage. |
| [Hunt damage](2026-09-30-hunt/REPORT.md) | Hunt-specific damage audit and retest. |
| [Combat](2026-09-30-combat/REPORT.md) | Source/answer checks for movement, damage, and wounds. |
| [Timing and Age](2026-09-30-timing-age/REPORT.md) | Timing and milestone cases. |
| [Fixes and retest](2026-09-30-fixes/REPORT.md) | Frozen cases after routing and source repairs. |
| [Citation smoke test](2026-09-30-citations/REPORT.md) | One live response checking generated citation prose. |
| [Community scenarios](community/KDM_Community_Test_Questions.md) | Source-guided development cases; community replies were visible during collection, so these are not blind holdouts. |
| [Enraged and Grasp](2026-10-02-enraged-grasp/REPORT.md) | Bounded level 1 compound source audit. Full Enraged remains unreviewed. |

## Dormant method experiments

| Evaluation | Purpose |
| --- | --- |
| [Size Up OCR](2026-10-02-size-up-ocr/REPORT.md) | OCR diagnostic and image-checked corrections. |
| [Claw and Grasp OCR](2026-10-02-claw-grasp-ocr/REPORT.md) | OCR diagnostic with profile-field omissions. |
| [Wiki extraction](2026-10-05-wiki-extraction/REPORT.md) | Local structured drafts from staged revisions. |
| [Maul preview](2026-10-07-maul-preview/REPORT.md) | Manually composed unreviewed-draft preview. |
| [Wiki preview](2026-10-07-wiki-preview/REPORT.md) | Isolated model-backed draft-answer tests. |
| [Wiki selection](2026-10-07-wiki-selection/REPORT.md) | Bounded draft selection and live previews, outside runtime retrieval. |

## Project organization

- [Folder audit](2026-10-24-folder-audit/REPORT.md): pre-cleanup findings; its proposed moves are now historical recommendations addressed by the cleanup.
- [Cleanup record](2026-10-24-folder-cleanup/REPORT.md): relocations, preservation, dependency changes, and checks.

## Reading and rerunning results

The active automated suite is `kdm-assistant/test_*.py`. Dated `run.py` files are saved experiment harnesses; some make paid model calls, stop if results already exist, or read sibling cases. Keep their directory depth and frozen outputs. Do not use them as routine test runners or overwrite their records.

Reports should be read before raw results. Follow the user's confirmation requirement for files above 1 MB and raw datasets above five rows. Historical filenames and workspace snapshots remain intact; use the [relocation map](../docs/history/README.md) when a source moved. New evaluations should state tested version, modes, exposure to expected answers, grading criteria, and limitations.

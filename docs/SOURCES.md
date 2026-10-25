# Sources and review workflow

## Evidence and review

The supplied scan is treated as edition 1.5 under the project's established convention. It does not establish compatibility with 1.6. Reviewed cards use the group's physical 1.5 photos or readable faces pictured in that rulebook.

1. Select evidence required by the release checklist or a documented answer failure.
2. Establish source identity, edition/provenance, and readable text/images. A filename or catalog path is insufficient.
3. Review the complete mechanical unit: ordered targets, profiles, conditions, triggers, diagrams, continuations, and linked definitions. Preserve omissions and uncertainty.
4. Add a reusable record with source links and bounded interpretation. Unreviewed candidates stay outside runtime retrieval.
5. Check neighboring questions, exceptions, source selection, and citations. Preserve the audit; distinguish development cases from independent evaluation.

The building assistant's summaries do not imply independent human verification or complete page transcription. Card and general-rule answers may require several sources. Ground Fighting's exact spatial zone remains an image reference.

## Inventory and preservation

| Location | Role | Preservation |
| --- | --- | --- |
| [Original scan](../sources/781787312-KDM-Rulebook-1-5.pdf) | Original source PDF | Tracked. Keep alongside the distinct focused derivative. |
| [Focused rulebook](../sources/KDM_Rulebook_1.5_Rules_Focused.pdf) | Retained pages with revised numbering | Tracked; regeneration input. |
| [Page map](../sources/KDM_Rules_Focused_Page_Map.md) | Revised, printed, and original identifiers | Tracked; asset preparation input. |
| [Served pages](../kdm-assistant/public/pages/) | Rulebook evidence shown by the app | Tracked runtime assets; keep in place. |
| [Served cards](../kdm-assistant/public/cards/) | Card citations and published physical-photo copies | Tracked runtime assets. |
| [Local original images](../kdm-assistant/data/card-reference-images/) | Original and supplementary image evidence | Ignored by Git. Preserve separately; absent from a fresh clone. |
| [Wiki candidates](../kdm-assistant/data/wiki-candidates/) and [drafts](../kdm-assistant/data/wiki-drafts/) | Unreviewed revisions and structured drafts | Ignored by Git; preserve as dormant evidence. |
| [Page manifest](../kdm-assistant/data/manifest.json) | Runtime page mappings | Tracked despite the general `data/` ignore rule. Startup supersedes stored review flags from current records. |
| `kdm-assistant/data/history.sqlite3` | Local conversations and pending corrections, when created | Local user data; preserve separately. Corrections do not overwrite reviewed rules. |
| [Evaluations](../evaluation/INDEX.md) | Source audits, failures, and regression history | Tracked evidence with dated scope and limits. |

`data/source-manifest.json` is an optional preparation output, not a required existing input or current coverage inventory. [Coverage](COVERAGE.md) describes reviewed topics. `records.py`, `core_records.py`, and `early_campaign_records.py` hold runtime summaries and tables. Sol receives linked-image availability, layout notes, and explicit interpretation limits alongside reviewed text. It receives no image pixels in the current text request.

## Asset preparation and numbering

Normal use relies on existing images and the page manifest. If the local server finds the manifest missing, it invokes `prepare.py`. That tool reads the map under `sources/`, reuses served pages, and can render the focused PDF using Poppler's `pdftoppm` when needed. A legacy external `work/pdf-triage` lookup remains for older workspaces; the active checkout does not require that folder.

Use revised PDF numbering for questions/navigation while retaining printed and original identifiers in citations. Historical reports' old root-level PDF paths refer to the same sources now under `sources/`.

## Dormant approaches

[OCR/catalog plans](history/research/ocr/) preserve paused Simulator extraction and method screening. [Wiki instructions](history/research/wiki/README.md) preserve isolated intake and preview commands. Neither is the current intake queue. Wiki drafts remain unreviewed where separate physical or rulebook evidence supports a reviewed record.

Ignored evidence is not disposable cache. Historical paid evaluation harnesses are not routine tests; preserve their dates, call limits, and saved results. The [evaluation index](../evaluation/INDEX.md) distinguishes them from the active regression suite.

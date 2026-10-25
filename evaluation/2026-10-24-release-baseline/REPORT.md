# First-release baseline results, 24 October 2026

## Result

The first release is not ready. Both modes completed all 36 turns across 32 scenarios. Sol produced 30 model answers; six turns stayed on deterministic clarification, unsupported, or edition paths. There were no request failures, fallbacks, retries, or unexecuted turns.

Sol supplied useful combined answers and often recognized missing evidence after retrieval had selected an adjacent record. Shared routing and context failures still blocked answerable questions before model composition, while required early-campaign coverage remains open. This run does not close a release coverage row or establish independent accuracy.

## Execution and preservation

- Actual `rules-v2` local HTTP handler, isolated temporary chat history, and an automatically assigned loopback port. Each scenario started a fresh conversation; the four two-turn scenarios used their actual returned chat identity.
- Local-only mode ran first, followed by Sol-requested mode, against the same unchanged questions, records, retrieval, handler, and model prompt. Their SHA-256 fingerprints before and after matched.
- Base commit: `dc6f312`, with the pre-existing dirty worktree recorded in `run-metadata.json`. This includes the uncommitted card-coverage and folder-cleanup work, so the commit alone is not the tested app snapshot.
- Executed 24 October, approximately 9:09–9:11 p.m. America/Chicago. Raw timestamps are UTC on 25 October.
- The user authorized reading the key from `D:\Documents\KDM\KDM-Rulemaster\.env` after the initial local configuration check found no key here. It was loaded into the evaluation process environment only. It was not printed, saved in results, copied into this checkout, or written back. No file in `main` was modified.
- Thirty successful API calls used 24,745 input and 3,945 output tokens, totaling 28,690. No speculative cost estimate is included.
- All 72 first responses are preserved under `responses/local/` and `responses/sol/`, one JSON file per turn. Metadata, question/app fingerprints, mode counts, and usage totals are separate. `run.py` refuses to overwrite first-pass metadata or repeat the paid run.

The harness observes the existing handler and model response usage without adding reviewer hints or changing answer behavior. The answering app receives only the fixed question, normal mode flag, and actual chat identity for follow-ups. No direct record/table selection, revised prompts, or patched sources were supplied.

## Response review

Assistant-graded from the frozen reviewer targets, actual answers, selected sources, inspected rulebook images, and prior card-image audits. The table below grades the response to the question. Evidence relevance, sources, and context are separate dimensions in [grades.csv](grades.csv); [GRADES.md](GRADES.md) explains every turn.

For a required coverage gap, a response pass means it acknowledged the missing evidence without inventing a ruling. It does not mean the required capability is delivered. No overall readiness or accuracy percentage is reported.

| Turn category | Turns per mode | Local pass / partial / fail | Sol-requested pass / partial / fail |
| --- | ---: | --- | --- |
| Topics with relevant reviewed coverage | 20 | 10 / 7 / 3 | 15 / 2 / 3 |
| Required source/record gaps or incomplete rule units | 13 | 2 / 2 / 9 | 12 / 0 / 1 |
| Initial missing-card clarification | 1 | 1 / 0 / 0 | 1 / 0 / 0 |
| Excluded event lookup and other-edition boundary | 2 | 1 / 0 / 1 | 1 / 0 / 1 |

Response totals are local 14 pass, 9 partial, 13 fail; Sol-requested 29 pass, 2 partial, 5 fail. Some successful Sol declines still carry irrelevant adjacent citations, and therefore fail evidence/source relevance despite passing the response boundary. These totals should not be read as full-source or release acceptance passes.

## Process failures to repair first

1. **Question scope can select an adjacent subject.** Q16 asks for Chomp after Claw has finished; local lookup returns Claw's instructions. Q20.1 asks about the Prologue but selects standard deployment, and Sol then falsely says the First Story source is needed even though that record exists. This requires subject/phase selection that respects what the question asks, rather than first lexical/card matches.
2. **Age attracts unrelated questions.** Aftermath Q06 and excluded hunt-event 84 in Q25 both receive an Age-milestone clarification. These responses never reach Sol. Missing coverage should produce a relevant limit, not a question about an unrelated table.
3. **Milestone and roll wording does not transfer.** Q29 identifies the first heavy-bordered Hunt XP box and a total of 13, yet asks which milestone. Q30's final 6 wording bypasses exact table resolution; Sol can recover the first outcome, while local mode returns generic instructions. The second Sol answer picks the correct Branding branch/band but asks for a new roll despite a supplied current roll, so it is partial.
4. **A corrected location loses the intended table.** Q31.1 correctly declines unreviewed Arms. Q31.2 changes the location to Head, which is reviewed, but selects hunt damage. Sol falsely says the Head table is absent and describes two Head injury boxes. The starter record sheet shows a single Head injury box, and Head 8 is Concussion in the reviewed table. This is an evidence/context failure with a material added rules error.
5. **Model prose is unaware of available image citations.** Q13 correctly distinguishes movement from activation under Ground Fighting, but says its diagram is missing. The response includes a card citation to the existing rulebook diagram. The model receives text without the actual picture or image-availability metadata; the user-facing result should not imply the app lacks the cited source.

The fixes should generalize across named subjects, phase/table identity, changed context, and natural roll wording. Do not add answers keyed to these exact questions. Preserve these cases as development/regression fixtures after any repair and use a new unseen set before release.

## Required coverage remains separate

The baseline confirms gaps in victory/aftermath, complete Chomp/Terrifying Roar/Enraged instructions, standard encounter/deck setup, First Day and settlement sequence, Language/unlocks, crafting procedure, Tall Grass effects, hunt procedure, and non-Head severe injuries. Full eligible AI/hit-location deck inventories are still needed to complete the release promise.

Several gaps concern reviewed runtime records rather than absent files: the supplied rulebook already pictures the victory rule and other early procedures. Head is an existing reviewed table that failed selection. Source acquisition, source promotion, and retrieval repair must be tracked separately. Correct missing-source responses from Sol do not close these requirements.

Cunning had no evaluation case or active source work. Other editions remain unverified. No source record was promoted or modified during this run.

## Source and citation checks

Inspected revised rulebook images 6, 8, 12, 13, 14, 15, 41, 44, 45, 47, 62, 81, 90, and 120 for the decisive starting, targeting, trap/persistence, victory, hunt damage, injury, Age, table, diagram, and deployment checks. Each is below 1 MB. Large PDFs and physical-card JPEGs were not reopened. The physical-card checks rely on the earlier photo audit and reviewed record text, so this is not a new independent card transcription audit.

Structural validation across the 72 saved responses checked 238 rulebook source references and 50 local card-image references. Revised/printed/original mappings matched the page map and all referenced local targets exist. The one unique external community URL was not fetched. Target existence is distinct from whether the selected source supports the question; irrelevant attached references are listed in the grades. No browser/device click test was performed.

## Limits and next work

The questions were authored with prior exposure to sources and regressions. This is a source-guided, assistant-graded development baseline, not a blind test or a general accuracy estimate. Context is the app's current stored structured context, not a model supplied with a complete conversation transcript. Six Sol-mode turns did not call the model because of local gates. The input hashes describe key answering inputs, not a hash of every file in the project.

No application code, answer records, model prompt, or sources were changed. The last recorded automated suite remains 101 passing tests from cleanup; it was not repeated for this evaluation-only task. The temporary server and database were closed, and the key existed only in the finished process environment. No deployment, push, or commit was performed.

Next: repair the subject/phase/table and follow-up failures using general behavior, then rerun affected saved cases as regression checks. In parallel planning, prioritize already-available fixed early rule units and missing required card faces/deck inventories. Complete remaining coverage and a new final evaluation before group-use and hosting checks.

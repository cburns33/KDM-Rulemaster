# Retrieval, table, and follow-up regression, 24 October 2026

## Result

Implemented general source-selection, roll-parsing, and follow-up fixes in `rules-v2`. All 115 automated tests pass. The final HTTP rerun completed 16 affected scenarios, 20 turns per mode, with all 40 targeted source/table decisions passing. Three answers used Sol; the remaining Sol-requested turns used deterministic table, clarification, or unsupported handling. No requests failed and no fallback responses were counted as model answers.

The original release baseline is preserved. These are development/regression results, not new holdouts, a complete answer-quality score, or release approval. Required evidence remains missing and the app still has 25 reviewed topics across 28 source pages.

## What changed and why

### Primary evidence selection

`reference_candidates` requires meaningful topic evidence before promoting a fuzzy search hit into a primary reference. It excludes unmentioned named cards and unidentified tables from that fallback. Common shared words alone should not turn a missing victory, crafting, or phase rule into an unrelated reviewed answer. Direct record selections, named reviewed cards, and identified table subjects retain their explicit paths.

Named missing sources are represented as coverage metadata in `records.py`: Chomp, Terrifying Roar, complete Enraged instructions, First Day, Language, and hunt-board procedure. These entries contain no card text or invented rules. The same guard handles their names and requested detail across phrasings. Enraged's missing full-card entry/flow is kept separate from the already reviewed level 1 Grasp/token example.

Completed card mentions are treated as background, including a later occurrence of the same active card. Thus a completed Claw does not replace the requested Chomp or Terrifying Roar. The former single Chomp question pattern was removed. Prologue setup is selected from positive encounter/setup context, with negated Prologue mentions excluded when the user switches to standard deployment.

These remain lexical scope heuristics with a finite source inventory. They do not establish unrestricted natural-language intent recognition; unrelated wording and ambiguous multi-source questions still need fresh evaluation.

### Table identity and roll grammar

Age is no longer selected solely because it ranked as a fuzzy hit. It needs an Age/milestone identity, a milestone XP value/box, explicit selection, or a compatible short follow-up. A mention of rewards and Hunt XP does not establish an Age event. Numbered table requests require an identified reviewed table; an unreviewed hunt-event result no longer opens an Age clarification.

Roll parsing accepts natural connecting words, including a total, a final roll, is/was, and still, while preserving prior compact inputs. XP values alone do not become rolls. Ordinals attached to Hunt XP milestone boxes identify the milestone; unrelated uses of first elsewhere in a sentence do not.

Both Hands of Heat branches now use the supplied result on the proper table when the settlement state changes. Resolved Branding prose says that it uses the supplied roll, so it does not ask for another roll after resolving the current 6.

### Context after an unsupported injury

Declining an unreviewed severe-injury location now retains the injury topic and location without pretending that a reviewed record exists. A follow-up correcting Arms/Legs to Head can select and resolve the actual Head table. Explicit new table or damage topics can leave that pending injury context. This behavior is checked through both local stored history and the hosted browser-context contract.

No new rules were ingested. No question-specific answer text, prompt snippets, frozen question IDs, or expected outcomes were inserted into production routing. Cunning and the model prompt were unchanged.

## Verification

Fourteen new automated test methods cover natural roll grammar, XP ordinals, unrelated table/reward questions, named missing sources, completed card mentions, encounter changes, injury-topic corrections and exits, changed oven state, and bounded versus full-card coverage. The suite now passes 115 tests. New local HTTP and hosted tests verify that context survives an unsupported injury and resolves a corrected location.

The nine initial scope-test methods failed on the old implementation in thirteen assertions/subtests, reproducing the target failures before fixes. Neighboring cases added during development check that the new guards do not capture an explicit new event or suppress the reviewed Enraged/Grasp interaction.

The final rerun uses the unchanged version 1 questions from the baseline and an isolated temporary database/port. Every selected scenario starts a fresh chat; the four paired scenarios preserve actual chat identity. `CHECKS.md` and `checks.csv` contain the before/after source/table decisions. Examples:

| Case | Final behavior |
| --- | --- |
| Q05–Q06 | Missing victory/aftermath coverage is stated without a trap or Age substitution. |
| Q16–Q18 | Complete missing AI instructions receive a named source boundary. |
| Q20.1 | The Prologue selects First Story and its fixed setup. |
| Q20.2 | Standard deployment is separate; complete standard deck composition remains a coverage gap. |
| Q25 | Hunt-event 84 receives an unsupported-table response instead of Age. |
| Q29 | First Age, total 13, resolves to the reviewed 7–15 band and proficiency qualification. |
| Q30 | Supplied 6 resolves first to Experiment 4–6, then to Branding 4–7 after the state changes. |
| Q31 | Arms is declined; the corrected Head 8 resolves to Concussion and its listed effects. |

All forty final source/table checks passed. That count includes correctly stated gaps; those are not completed release capabilities. Local Q19.2 remains a reference naming Sniff rather than a composed no-attack explanation. Local Q20.2 still lacks full deck evidence. Final model-generated Q19.2, Q20.1, and Q20.2 were inspected in full; their target/encounter handling is correct within the supplied evidence.

Exact table answers now bypass Sol for these cases, removing the earlier opportunity to invent Head injury-box details or request a redundant roll. This proves the repaired deterministic path on these prompts, not improved model reasoning about every injury or table.

## Artifacts, calls, and preservation

- [Final run](final/): 40 first responses for the final app snapshot, metadata, and summary. Three successful Sol calls used 1,526 input and 373 output tokens, 1,899 total. The answering inputs matched before and after this run.
- Root `responses/` and metadata: the initial development rerun, retained before the final Branding wording and bounded-source refinement. Three successful Sol calls used 1,853 tokens total.
- `table-wording/`: four deterministic HTTP responses after the Branding wording change, with no model calls.
- Total live calls for this repair task: six successful calls, 3,052 input and 700 output tokens, 3,752 total. There were no automatic paid retries. Distinct development snapshots and the final run remain separate.

The user-authorized key file was read in memory for the evaluation processes. No key was copied, printed, or stored in the artifacts, and no file in the separate `main` checkout was modified. Temporary servers/history closed after the runs. No deployment, commit, or push was performed.

All 81 original baseline files, excluding generated Python caches, retained the same aggregate filename/content SHA-256 before and after this task:

`cb83fceb0887be0f9bf7a995fc071fa87653a81225b769330719cb31108e2e0d`

The baseline questions, responses, grades, report, metadata, and harness were not edited. The regression harnesses read them and write only to this new directory. `git diff --check` passes.

## Remaining work

Complete the missing required victory/aftermath, opening cards/deck inventories, settlement, hunt, terrain, and injury records from verifiable sources. The earlier Ground Fighting image-availability messaging issue was not part of these retrieval/table/follow-up changes and remains open. Fresh source selection, multi-card/context, and explanation questions are still required after coverage and process work before release. Launch identity, device checks, protected hosting, and group play validation remain on the checklist.

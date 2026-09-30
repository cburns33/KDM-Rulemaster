# Timing and Age source audit, 30 September 2026

## Outcome

Seven scenarios were tested in local and Sol-enabled modes through the production HTTP handler. The batch reproduced incorrect Encourage timing and incorrect Age table selection, confirmed missing attacker-knockdown coverage, and found an Age follow-up context failure. No application code or reviewed records were changed in this batch.

Three GPT-6 Sol calls used 2,115 input and 460 output tokens, totaling 2,575 tokens. The remaining Sol-enabled requests were handled locally. All 49 existing automated test methods passed.

## Method and limits

- Baseline: main at a6d1a98 plus the uncommitted hunt-event fix and source record from earlier today.
- Prompts and expected behavior were saved before requests. Each case and mode had a fresh chat, except T07, which continued T04.
- A temporary database isolated the test from normal app history. The production server was not restarted or modified.
- The evaluator inspected complete page images from the supplied edition 1.5 scan. This is an unblinded assistant-graded source audit of known risk areas, not a general accuracy score or independent human review.
- One model sample per eligible question. No retries or prompt tuning.
- Saved artifacts: run.py, questions.jsonl, results.jsonl, run-metadata.json.

## Results

| Case | Scenario | Local result | Sol-enabled result |
| --- | --- | --- | --- |
| T01 | Two survivor hits; first reaction knocks attacker down; another survivor Encourages them. Can the second hit continue? | Retrieves monster damage rules and misses cancellation. | Abstains on cancellation, but incorrectly requires a survival opportunity for Encourage. |
| T02 | Eligible helper Encourages during survivors' turn outside a survival opportunity. | Supplies survival record without the decisive any-time rule. | Incorrect: says to wait for a survival opportunity. |
| T03 | First Age milestone, 2 Hunt XP, roll 8. | Correct table and roll reward: one random fighting art. | Same local resolution; no API call. |
| T04 | Second Age milestone, 6 Hunt XP, asks which table to use. | Returns first-milestone reference with a later-milestone coverage disclaimer. | Safe partial answer: identifies second milestone and says its table is missing from reviewed evidence. |
| T05 | Second Age milestone, 6 Hunt XP, roll 8. | Incorrect: uses milestone 1 and awards a fighting art. | Same incorrect local resolution; no API call. |
| T06 | Age roll 8 without a milestone. | Assumes milestone 1 instead of asking. | Same local resolution; no API call. |
| T07 | Follow-up to T04: I rolled 8. What do I gain? | Switches to a severe-injury location clarification. | Same irrelevant clarification; no API call. |

T03 validates only the roll reward and table selection. Its resolved answer omits the milestone's weapon-type selection instruction, which remains in the attached record. It is not a complete milestone walkthrough.

## Source findings

Page references use revised PDF / printed book / original PDF numbering.

- 50 / 73 / 77, Knocked Down Survivors: a survivor knocked down during their attack has unresolved hits canceled. Standing later does not restore canceled hits.
- 55 / 78 / 82, Encourage: a standing survivor spends 1 survival to let another knocked-down survivor stand; Encourage permits any-time use. Deaf survivors cannot be encouraged. Action availability, once-per-round limits, the attacker's restriction, and unresolved survival actions remain relevant.
- 55 / 78 / 82 and 56 / 79 / 83: Dash and Surge use survival opportunities. The surrounding opportunity rules should not erase Encourage's specific timing permission.
- 24 / 43 / 47: the Hunt XP track and milestone count determine which Age rules apply.
- 81 / 107 / 111: milestone 1 is Weapon Proficiency; milestone 2 is Improved Reflexes. A roll of 8 gives one random fighting art on milestone 1 and +1 permanent strength on milestone 2. Without a milestone, the roll is ambiguous.

## Causes

1. Missing rules in source records: survivor-attack-sequence omits attacker-knockdown cancellation. survival-actions omits Encourage's any-time permission and deaf-recipient restriction.
2. Retrieval: T01 selects monster-hit-damage rather than the survivor attack rules.
3. Deterministic table selection: Age milestone wording forces age-first-milestone, then an explicit roll resolves its first table without validating which milestone was requested. Sol is bypassed for resolved results, so selecting Sol cannot correct this error.
4. Conversation scope: the second-milestone question retains only the first-milestone record ID. The generic follow-up is searched afresh and enters the Head-injury clarification before Age context can be used.

## Recommended next change

Add failing regression tests for these exact cases and nearby controls. Complete the attacker-knockdown and Encourage rule units, route the attack question to the relevant evidence, and validate Age milestone identity before resolving a roll. Preserve milestone context in follow-ups; ask when it is missing and reject unsupported milestones until their tables have reviewed coverage.

Then rerun the automated suite and this targeted batch with a small paid-call cap. Broader holdouts can follow after these failures are resolved.

## Repository state

This evaluation and its project-status update are local and uncommitted. Earlier hunt-fix changes remain untouched. No push was made.

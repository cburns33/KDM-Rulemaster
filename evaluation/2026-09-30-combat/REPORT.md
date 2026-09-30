# Combat source audit, 30 September 2026

## Outcome

Six scenarios ran in both local and Sol-enabled modes. None received a complete direct ruling from Sol. All six produced missing-evidence or partial responses. No definite incorrect ruling was identified in this batch. This does not resolve the wrong answers found in the earlier timing and Age audit.

Local lookup returned related reference text in all six cases, without enough information to settle the question. The selected source records omit rules visible in the supplied book.

## Method and limits

- Tested main at a6d1a98 plus the existing uncommitted hunt fix. No app code, reviewed records, or model prompt changed during this batch.
- Questions and expectations were saved before responses. The evaluator had seen earlier findings on these topics. This is an unblinded, assistant-graded audit of known coverage risks and contrast cases, not an accuracy benchmark.
- Used the production HTTP handler with a temporary history database. Each case and mode used a fresh chat. Normal app history was untouched.
- Six live requests completed, each on its first attempt. No paid retries or answer tuning.
- Visually inspected complete revised PDF pages 9, 45, 46, 51, 53, and 135.
- C02 has a wording limitation: “survivor ... facing the lion” should say the survivor is in front of the lion, in the area the lion faces. Survivor orientation does not define this targeting condition. Its expected first-condition ruling assumes the latter. Preserve this limitation when interpreting the case and correct the wording in a future test.

## Findings

### C01: Monster movement after moving earlier in the round

Expected: the instructed Basic Action includes Move & Attack Target. The monster can move again up to its current movement value until adjacent; earlier movement does not exhaust a round-wide allowance.

Local retrieval selected moods-and-flows and priority-target. Sol declined to decide because its records omit Basic Action movement and how the allowance applies. Safe abstention, with incomplete retrieval and source coverage.

### C02: Claw versus Basic Action targeting

Expected under the intended facing condition: Claw selects the qualifying standing threat. Basic Action selects the closest survivor in field of view, which can be knocked down. A knocked-down survivor is not a threat in the stated circumstances.

Local retrieval selected white-lion-claw, which omits both the threat definition and Basic Action target list. Sol gave a conditional Claw answer, then identified both missing rules. It did not settle Basic Action. Partial response. The wording caveat above prevents treating this as a clean targeting pass/fail.

There is also a wording risk in the Claw record itself: “threat facing the White Lion” should express the monster's facing area.

### C03: Wound threshold and Failure reaction

Expected: die 4 + weapon strength 3 + survivor strength 2 = 9, meeting toughness 9, so it wounds. Die 3 totals 8 and fails. The Failure reaction applies only to the failed attempt.

Local retrieval selected survivor-attack-sequence plus survival-actions. Sol stated the success/failure reaction distinction but could not calculate either outcome because the record omits the formula and threshold. The attack record cites the page containing this formula. Partial response caused by incomplete extraction.

### C04: Luck-based critical below toughness

Expected: natural 9 with +1 luck critically wounds a location with a critical effect, despite a total below toughness. Perform the critical effect and cancel Reflex. Impervious and monster luck were excluded.

Local retrieval supplied only critical-wound-examples. Sol identified the critical/Reflex example but declined to resolve the below-toughness case without the general rule. Safe partial response.

### C05: No critical effect

Expected: a location without a critical effect cannot be critically wounded. Luck does not turn a natural 9 into a lantern 10. With a total below toughness, the attempt fails.

The same examples record was selected. Sol declined to infer the general luck and toughness rules from the examples. Safe missing-evidence response.

### C06: Impervious contrast

Expected: the natural 9 with +1 luck causes a critical result and its effects, with Reflex canceled. Impervious prevents the monster wound.

The same examples record was selected. Sol identified the missing Impervious interaction and declined to settle the three consequences. Safe missing-evidence response.

## Source map

| Revised PDF | Printed book | Original PDF | Relevant content |
|---:|---:|---:|---|
| 9 | 27 | 31 | White Lion Basic Action, Claw, Sniff, targeting explanation |
| 45 | 68 | 72 | Pick Target, threat, facing, field of view |
| 46 | 69 | 73 | Move & Attack Target and monster movement |
| 51 | 74 | 78 | Wound formula, threshold, wound steps, reactions |
| 53 | 76 | 80 | Critical wounds, luck, Impervious exception, canceled reactions |
| 135 | 232 | 236 | Movement and Move & Attack Target glossary entries |

Source: KDM_Rulebook_1.5_Rules_Focused.pdf. Edition 1.6 remains unverified.

## Verification and API usage

All 49 existing automated test methods passed. These tests do not establish coverage of the six questions above. All twelve evaluation HTTP requests succeeded.

Six GPT-6 Sol calls used 2,911 input tokens and 990 output tokens, totaling 3,901 tokens. No dollar estimate was calculated.

Artifacts beside this report:
- run.py: bounded harness, refuses a paid rerun if results already exist.
- questions.jsonl: frozen prompts and expected rulings.
- results.jsonl: exact responses.
- run-metadata.json: source payloads, model, working-tree state, and usage.

## Next work

Fix the confirmed timing and Age errors first. Then complete the core source units for monster movement, threat and facing definitions, the White Lion Basic Action, wound calculation, and critical-wound exceptions. Add regression tests for the contrasts above, correcting C02's facing wording. Retest with bounded live calls after source and routing fixes.

No application fixes, new automated tests, commit, or push occurred in this batch. Existing hunt changes and all September 30 evaluation artifacts remain local and uncommitted. The project status file has the handoff state for /compact.

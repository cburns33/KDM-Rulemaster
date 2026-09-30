# Fix verification, 30 September 2026

## Result

The retest met the core ruling and safety expectations for all 13 scenarios. Eight live Sol answers supplied supported rulings for the timing and combat questions. Five Age cases stayed local: one resolved the first milestone, three refused an unreviewed second-milestone result, and one requested the missing milestone.

This is a regression result for known cases. It does not establish general answer accuracy or verify later Age tables.

## Case results

| Case | Result in Sol-enabled mode |
|---|---|
| T01: attacker knocked down, then Encouraged | Unresolved hits remain canceled. Standing does not restore the attack. |
| T02: Encourage on the survivors' turn | No Dash/Surge opportunity is required under the stated conditions. Shared restrictions are retained. |
| T03: first Age milestone, roll 8 | Local resolution grants a random fighting art and includes weapon-type selection and the lifetime limit. |
| T04: second Age milestone, no roll | Local response identifies missing table coverage. |
| T05: second Age milestone, roll 8 | Local response refuses to substitute the first table. |
| T06: Age roll without milestone | Local response asks which milestone. |
| T07: roll follow-up to T04 | Second-milestone context persists; no switch to severe injuries. |
| C01: Basic Action after earlier movement | New movement instruction can move the monster again; reaching the target remains conditional on current movement. |
| C02: Claw versus Basic Action | Claw selects the qualifying standing threat; Basic Action selects the closest survivor, including the knocked-down survivor. |
| C03: wound threshold and Failure | 4 + 3 + 2 meets toughness 9 and avoids Failure; 3 + 3 + 2 fails and triggers Failure. |
| C04: luck-based critical below toughness | Wound and critical effect occur; Reflex is canceled. |
| C05: no critical effect | Natural 9 with +1 luck fails when below toughness and the location has no critical effect. |
| C06: Impervious | No monster wound; critical effect occurs and Reflex is canceled. |

Local mode returned the corrected reference records for the eight general rules questions. It does not synthesize a conversational ruling for those questions. Its five Age responses matched the Sol-enabled mode because those cases bypass the API.

## Method

- Reused the frozen timing/Age and combat scenarios through the production HTTP handler.
- Corrected C02's facing wording before requests: the standing survivor is in the area the lion faces. Saved both the original wording and the correction.
- Each case and mode had a fresh chat, except T07 followed T04.
- Used an isolated history database; normal app chat history was untouched.
- Eight API calls completed on their first attempt. No retries, extra calls, or model-prompt changes.
- Assistant-graded against the previously reviewed rulebook evidence and frozen expectations. The source additions and routing fixes were informed by these cases, so this is an unblinded regression retest.
- All 26 local HTTP requests succeeded.

## Remaining presentation issue

T01's generated prose included “p. 77,” “p. 82,” and “p. 81” without identifying them as original-PDF page numbers. These correspond to record identifiers supplied to the model, rather than the revised PDF numbering used by the app. Its clickable source objects retain the correct revised, original, and printed mappings.

This did not change the ruling, but the prose can confuse users. A future citation fix should keep generated page references aligned with the app's mapped citations. The captured raw response was preserved.

## Verification and usage

All 62 automated tests passed after this retest. The application health check reports 17 records, 138 retained pages, and Sol configured. The source inventory has 23 reviewed pages. No further application changes or restart were needed in this retest turn.

Eight GPT-6 Sol calls used:
- Input: 7,375 tokens
- Output: 880 tokens
- Total: 8,255 tokens

No dollar estimate was calculated.

## Files and next step

This directory contains run.py, questions.jsonl, results.jsonl, and run-metadata.json. The result files preserve exact responses, selected source payloads, request status, usage, and the working-tree state.

Project status is updated. The fixes and September 30 evaluation artifacts remain local and uncommitted. Nothing was pushed.

Next: address generated page-reference consistency, then collect fresh questions with new wording and counterexamples. Later Age milestones and other injury tables still need reviewed coverage. This is a safe point for /compact.

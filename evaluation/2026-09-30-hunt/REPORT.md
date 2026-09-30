# Hunt-event damage test, 30 September 2026

## Outcome

The current build failed this question in both local lookup and Sol-enabled modes. It returned an unrelated missing-injury-table notice. No model request occurred, so this run consumed no API tokens.

Tested commit: a6d1a98. The working tree was clean before this run. The test used the production HTTP handler in a fresh process, with a temporary history database and a new chat for each mode. It did not change application code, source records, or normal chat history.

## Frozen question

> During a hunt event, my survivor suffers 3 damage to the body. They have 1 armor in that location and 1 insanity. What happens to the remaining damage, and does it cause a severe injury or brain trauma?

Both modes returned status `unsupported`, with no record or citation:

> Only the severe Head injury table is reviewed in this collection. I cannot resolve the requested location from that table. Consult its severe injury table in the source browser.

This is a failure to answer a supported general damage question. The run did not reproduce the earlier incorrect model explanation because the local guard stopped the request before the model path.

## Source ruling

Visually checked the complete rendered rulebook pages using the PDF skill.

| Rule | Revised PDF | Printed book | Original PDF |
|---|---:|---:|---:|
| Event Damage; Severe Injuries and Brain Trauma | 41 | 63 | 67 |
| Deal Damage to Hit Locations | 47 | 70 | 74 |
| Brain Damage; Damage Outside of Attack Actions | 48 | 71 | 75 |

For ordinary hunt-event damage to the body:

- The first damage point removes the one body armor point.
- The remaining two points fill available body injury boxes in light-then-heavy order. If both boxes begin empty, both become checked.
- Insanity stays at 1. It protects the brain location and does not absorb body damage.
- Ordinary hunt-event damage does not cause severe injuries or brain trauma, even when available injury boxes are exhausted.
- Damage taken during the hunt carries into the showdown.
- An event can explicitly instruct a severe injury or brain trauma. Follow that instruction when present; it is a separate exception stated on the same hunt page.

The question leaves existing injury-box states unspecified. A complete answer should state the empty-box assumption or describe both cases. With two empty boxes, this scenario would not overflow into a severe injury even under normal damage rules, so an already-injured variation is needed to test the hunt exception in isolation.

## Diagnosis

The injury guard added on 29 September checks for an injury word together with “severe” or “table,” then refuses a named location other than Head. This question contains “body,” “severe,” and “injury,” so it is classified as an injury-table request despite asking whether an injury happens at all.

The guard prevented an unrelated Head-table answer, but it also blocks general damage questions. It needs to distinguish table-result requests from questions about damage consequences. The hunt-event exception remains missing from the reviewed source coverage identified in the earlier evaluation.

## Next work and acceptance checks

1. Narrow injury-table routing so questions about whether damage causes an injury reach the relevant damage rule. Preserve refusal of actual unreviewed Body, Waist, Arms, and Legs table results.
2. Add a complete hunt-event rule unit from revised PDF page 41, including nonlethal damage, carryover, and explicitly instructed severe injuries or brain trauma.
3. Verify this exact question, plus variants with already-filled injury boxes, actual brain damage, an explicit event instruction, and equivalent showdown damage.
4. Confirm the new source unit reaches the model, then run a bounded live retest.

The evaluator already knew this rule from the prior audit. This is an unblinded regression investigation, not an independent accuracy benchmark.

Raw HTTP responses and call count are saved in `evaluation/2026-09-30-hunt/result.json`. This report and the project status update remain local and uncommitted.

## Fix and retest, 30 September 2026

Narrowed the injury guard so damage-consequence questions can reach reviewed rules. Actual unreviewed injury-table results remain unsupported. Added a hunt-event damage record with the complete Event Damage and Severe Injuries and Brain Trauma rule unit, the token-duration continuation, and supporting damage-order and brain-damage rules. Hunt damage receives its phase-specific record; the tested showdown cases retain normal damage consequences.

Five new automated test methods cover the original question, filled injury boxes, brain damage, explicitly instructed injuries, carryover, switching away from Head-table context, unreviewed table refusal, edition checks, source delivery to the model, citation mapping, and saved history. The new scenarios reproduced failures before the fix. All 49 test methods now pass. Reviewed coverage is 16 topics on 22 source pages.

One live GPT-6 Sol retest used 563 input tokens and 104 output tokens, 667 total. It answered that 1 body armor is lost, the two empty body boxes become checked, insanity stays unchanged, and no severe injury occurs. It handled already-checked boxes and the explicit-event exception. It left the answer to the brain-trauma subquestion implicit in the body-versus-brain distinction. This is a supported core answer with a minor completeness omission.

The model retest used the same production HTTP path and isolated history as the baseline. Its supplied evidence was the new hunt-event record. The raw response and usage are in `retest.json`. Only this original question received a live model retest; the nearby cases were tested through local resolution and mocked HTTP integration. This is a regression check after adding the relevant rule and a matching worked example, not a new holdout.

Application changes, evaluation results, and documentation remain local and uncommitted. Next: address the other incomplete source units and Age milestone selection, then rerun the broader evaluation and collect fresh holdouts.

# Fixed-question draft selection and answer evaluation, 7 October 2026

## Method

The nine questions and expected sources in [QUESTIONS.md](QUESTIONS.md) were fixed before implementing `select_draft()`. The selector uses card-title matches first, then distinctive words from draft titles, card-text blocks, and linked-page names. It refuses a source when the evidence is absent or the top matches are too close. It reads only the three locally staged drafts and makes no wiki request.

Seven questions selected a draft and were sent to GPT-6 Sol with that single draft. Two questions declined selection before any model call. Exact generated previews from the first live run are in [live-results.md](live-results.md). The original checkout's existing API key was used in memory and was not copied into this worktree.

## Results

| ID | Selection | Answer assessment |
| --- | --- | --- |
| S01 | Maul, correct | Gave the remaining knocked-down target choice and Sniff fallback. |
| S02 | Maul, correct | Said Grab's definition is missing and limited the answer to Maul's target reference. |
| S03 | Combo Claw, correct | Gave Speed 2, Accuracy 4+, Damage 1. It also included other card text without conflicting with the source. |
| S04 | Combo Claw, correct | Kept the condition that the attack deals damage more than once before drawing an AI card. |
| S05 | White Lion Data Card, correct | Used the level 2 row: 10 Basic and 5 Advanced AI cards. |
| S06 | White Lion Data Card, correct | Described Sniff's turn-ending effect, threat duration, and level 3+ accuracy token. |
| S07 | White Lion Data Card, correct | Identified Cunning as a listed trait and declined to invent its effect. |
| S08 | No source, correct | Declined the Phoenix question before an API call. |
| S09 | Ambiguous, correct | Asked for a named card or action before an API call. |

All nine fixed selection decisions met their expected outcome. The seven model answers were grounded in the selected drafts. This is a small, preselected question set, not an accuracy estimate for unseen cards or arbitrary wording.

The first live results appended every mentioned wiki link, which produced distracting notices for terms such as `damage` and `White Lion`. The preview footer now identifies a missing linked page only when the question asks for that term's definition. Local checks cover the focused notices for S02 and S07. The saved live results preserve the original output; the footer edit did not change the model prompt or answer text.

## Limits and next source work

The command still handles one draft per answer. It does not combine a card with rulebook evidence, fetch linked definitions, establish physical 1.5 compatibility, or promote wiki text into reviewed records. The existing extraction report says the three card faces were compared with supplied photos, while the White Lion Basic Action section lacked that photo check. No local Maul, Combo Claw, or White Lion Data Card photo file is present in this workspace for a fresh physical-card audit. The linked Grab and Cunning definitions also remain outside the selected drafts.

The [source audit](SOURCE_AUDIT.md) visually checked the available Grasp image and relevant rulebook pages. The [combined Grab preview](combined-grab-preview.md) kept the checked Grab mechanic separate from Maul's unreviewed wiki target line and declined to certify a physical 1.5 Maul ruling. Fresh Maul, Combo Claw, and White Lion Data Card card-face images are still needed for direct edition checks before any draft enters reviewed retrieval.

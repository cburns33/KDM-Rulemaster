# Isolated wiki draft answer test, 7 October 2026

## Scope

Tested `kdm-assistant/wiki_preview.py` against the three locally staged, unreviewed drafts: Maul revision 28126, Combo Claw revision 28091, and White Lion Data Card revision 28563. Each request supplied one explicit draft and one question to GPT-6 Sol through the Responses API with `store: false`. The source URL, revision, unreviewed label, and unloaded linked-page notice are added by the local preview code. No new wiki request, OCR, reviewed-record change, `/api/ask` change, or deployment occurred.

The original checkout's existing API key was used in memory for this bounded test. It was not copied into this worktree. Five distinct questions and one repeated Maul question for the complete preview wrapper made six live API calls.

## Results

| Question | Expected from the staged source | Observed answer | Grade |
| --- | --- | --- | --- |
| What does Maul instruct the White Lion to do? | Preserve target priority, no-target Sniff, 2 / 2+ / 3 attack, and After Damage effects. | Gave the target order, Sniff fallback, attack profile, bleeding token, and knockdown. | Pass |
| What does Grab do on Maul? | Identify Grab as a linked definition absent from the supplied draft. | Said the draft does not define Grab and limited its answer to Maul's target reference. | Pass |
| When does Combo Claw draw an AI card, and what does Lost Hand say? | Keep the more-than-once damage condition and the persistent-injury effect. | Kept the condition and reported the adjacent-survivor understanding effect with its once-per-lifetime limit. | Pass |
| What are the level 2 White Lion deck, attributes, and trait? | Read the level 2 row without mixing adjacent levels. | Gave 10 Basic, 5 Advanced, no Legendary, movement 7, toughness 10, +1 speed, +1 damage, and Cunning. It flagged that Cunning's definition was absent. | Pass |
| Does the draft prove the physical 1.5 Data Card has the Basic Action shown? | Abstain from certifying the physical card; the supplied photo did not check this wiki section. | Declined the edition claim and described the wiki draft's Basic Action as unverified for the physical card. | Pass |

The repeated Maul question exercised `preview()` through a live model call. Its output included the unreviewed label, edition warning, revision, source URL, and unloaded linked-page notice. A subsequent presentation edit limits that notice to links mentioned in the question or answer; the unit test covers the edit without another live call.

## Boundaries and next check

The local request checks confirmed that each API payload contained only the selected draft's blocks and linked-page names. The three drafts differ in structure: Maul has target order and an attack table; Combo Claw adds a conditional draw and persistent injury; the White Lion Data Card has level rows, Sniff, and a separate Basic Action section. The preview command accepted all three without card-specific answer code. It does not select a draft from a question, resolve linked definitions, certify edition 1.5, or enter the app's reviewed answer path.

These six calls are a small functional check, not a held-out accuracy estimate. The next evaluation should test unseen card questions and source selection, then acquire verified linked definitions and physical 1.5 evidence before considering any draft for reviewed retrieval.

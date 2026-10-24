# White Lion card retrieval check, 24 October 2026

## Scope

The group identified six photos as cards from its physical 1.5 set. Four new reviewed app records cover Maul, Combo Claw, Power Swat, and Size Up. The existing Claw and Grasp records now link to the group photos. The card photos are served from `kdm-assistant/public/cards/` and the original copies remain in the ignored evidence folder. The Maul and Combo Claw text was checked against staged wiki revisions 28126 and 28091, then against the physical photos. The wiki drafts remain outside runtime retrieval.

Each new answer links the relevant card photo. Book page 71 supplies general attack effects; it is supporting context, while the photographed face supplies the card instructions. Maul also uses the photographed Grasp definition of Grab. These records cover the visible card text and the linked mechanics stated in their notes. They do not certify other White Lion cards or later editions.

## Question check

Twelve questions were written after the physical photo audit and before changing retrieval. The baseline selected the Claw record correctly for its Claw question. It selected adjacent records for the other eleven, including a White Lion record for an unrelated Phoenix question. A Size Up question was added for the final check. The final deterministic lookup selected the intended card on Maul, Combo Claw, Power Swat, Size Up, and Claw questions. It selected Maul with supporting attack and Grab records for the combined question, declined Cunning and Phoenix, and asked for a card name when the no-target question omitted one. All 13 final source decisions matched the expected category. The new card questions and boundaries are covered by regression tests.

The check exercised local source selection and record text. It did not make a live model call or measure accuracy across unseen card questions. The original twelve questions became development cases after the baseline run, so the final 13/13 result is a regression result, not an independent accuracy estimate.

## Verification and remaining limits

The Python suite passed 91 tests. The local server served the Maul JPEG with the expected media type, and `git diff --check` found no whitespace errors. The separate `main` checkout was untouched. Automatic Vercel deployments remain disabled for `rules-v2`.

Cunning's effect has no checked source and receives a source-needed response. The group's White Lion Data Card face has not been photographed; its wiki draft and the online image comparison remain outside reviewed retrieval. The app still has limited card coverage, and its named-subject guard covers only a simple question form. A fresh evaluation with unseen phrasings and compound questions is the next quality check.

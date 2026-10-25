# Fresh White Lion question check, 24 October 2026

The 15 questions and expected sources in `QUESTIONS.md` were fixed before this lookup run. They span target priority, conditional effects, a card and rulebook combination, two unsupported subjects, and an unspecified card. This check used the deterministic local resolver; no model call was made.

## First run

Fourteen of 15 questions received the expected primary card or decline status. The unspecified no-target question selected an unrelated Survival actions record. Maul's prior-Grab target question and Size Up's knocked-down-threat question selected the right cards but left their yes/no conclusion implicit. One Combo Claw question pulled in an irrelevant Grasp and Enraged record as secondary evidence. Some other answers carried unrelated White Lion setup or Claw summaries.

## Changes and verification

The no-target clarification now covers an unspecified eligible target without requiring a particular sentence opening. Secondary White Lion records are added only when their card name appears in the question; First Story setup requires First Story or prologue wording. Maul links both its own physical card and the Grasp photo containing the Grab definition. Its record states that selecting a prior Grab victim does not perform Grab again. The Size Up record states the knocked-down-threat and 1-3 roll boundaries.

After these changes, all 15 fixed questions returned the expected primary card or decline category. The previously implicit Maul and Size Up answers now state their conclusions, and the extra Grasp and setup citations disappeared from the checked questions. The full Python suite passed 92 tests. This second pass used the same questions for development and is a regression check, not an independent accuracy estimate.

## Limits

The app still returns long reference summaries in local mode, including some general rule context that a short answer would omit. The unknown named-subject guard covers a simple question form. Model-based synthesis, new card families, and the missing Cunning effect were not verified here. The next evaluation should use another unseen set with paraphrases, follow-up turns, and conflicts between card instructions and general rules.

## User-directed test substitution

After the first run, the user asked to drop the Cunning test and use a supplied card photo. Active question 13 now tests Maul's first target condition when its prior Grab victim is beyond movement range and a different knocked-down survivor is in range. The resolver selects Maul and links the group's Maul and Grasp photos. Its answer keeps the prior Grab victim first. The original Cunning response remains described above as historical run evidence; it is no longer in the active question set or Python tests. The runtime still marks Cunning's effect as unverified because the available data card lists the trait without defining it.

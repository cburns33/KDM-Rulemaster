# Community scenario test set

These prompts exercise the local reference assistant and its optional GPT-6 Sol explanation path. They are not blind evaluation: search results during collection included community replies. Expected behavior for the app is based on the supplied edition 1.5 scan, not community voting. No community answers are reproduced here. Tests check the selected evidence, material qualifications, and missing-source notices.

Sol is connected and off by default. When selected, it receives the current question and up to three reviewed records only if local retrieval finds a source-reference answer. Exact table results, edition checks, and missing-source notices stay local. Run new evaluation prompts through both local retrieval and Sol, then check the explanation against the cited pages. GPT-6 Astra is reserved for project-side source review and is excluded from the app answer path.

## 1. Early game: White Lion deployment

On the standard White Lion showdown setup, does "start within the blue zone" mean only the marked blue squares, or the whole area enclosed by them?

Source: https://www.reddit.com/r/KingdomDeath/comments/ela87k

Coverage: revised PDF 120, printed 179, original 183. Keep the prologue setup separate.

## 2. Universal mechanics: action timing

One survivor has completed movement next to the monster but has not activated a weapon. Can a different survivor, already near Tall Grass, Surge and use the activation to hide before the first survivor attacks?

Source: https://boardgamegeek.com/thread/1730963/question-about-when-you-can-use-survival-actions

Correction to the earlier chat prompt: the cited example involves activating the terrain's hiding effect. "Surge and move into tall grass" changed the action being tested. A nearby counterexample asks whether the attacking survivor can dodge a reaction after their attack has begun.

Coverage: revised PDF 55-56, printed 78-79, original 82-83. Survivor act/attack context: revised 50-51, printed 73-74, original 77-78.

## 3. Universal mechanics: multiple hits

A monster attack has Speed 2 and Damage 3, and both attack rolls hit. If the target is eligible to Dodge and cancels one hit, how is the remaining hit resolved? What additional survivor information would determine the final injury?

Adapted practice scenario from a community rules-reference post, rather than a standalone unanswered question: https://www.reddit.com/r/KingdomDeath/comments/e9plf6

Coverage: revised PDF 47 and 55-56, printed 70 and 78-79, original 74 and 82-83. Nearby cases include two hits to the same location and damage outside an attack profile.

## 4. Early-game interaction: permanent priority and Ground Fighting

A White Lion critical wound creates a permanent priority target, then Ground Fighting is in play. How do those effects interact?

Source: https://www.reddit.com/r/KingdomDeath/comments/1iq62di

Partial coverage: revised PDF 43-46, printed 66-69, original 70-73. Ground Fighting is pictured in the rulebook, but the exact Fuzzy Groin hit-location card text is missing from the reviewed sources. The app must flag that gap instead of claiming the complete interaction is established.

## Next evaluation step

Use additional community questions after expanding the corpus, keeping a set of questions out of development tests. Do not count passing these source-guided checks as evidence of general rules comprehension.

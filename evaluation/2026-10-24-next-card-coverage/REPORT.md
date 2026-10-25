# Next card coverage phase, 24 October 2026

## Result

Added three reusable reviewed records: Founding Stone gear, Strange Hand hit location, and Clever Ploy trap. The app now has 25 reviewed topics supported by 28 source pages. Each new record includes a clickable image of its card face in the supplied 1.5 rulebook. Ground Fighting's existing record now links its face and Zone of Death diagram. No new card image was required or generated.

## Source audit

The building assistant inspected the existing rendered page images. The source is the project's supplied rulebook scan, treated as edition 1.5 under the established project convention. These are scan-backed checks, with no new physical-set photo verification or independent human review. The new summaries preserve the mechanical instructions within their stated scope; they are not complete transcriptions of every page.

| Card | Revised / printed / original PDF | Evidence checked |
| --- | --- | --- |
| Founding Stone | 12 / 30 / 34 | Full face and labeled profile: melee, stone; Speed 2, Accuracy 7+, Strength 1; activation to sling from anywhere on board; archive for one automatic hit that inflicts a critical wound; archive returns gear to the game box. The adjacent text distinguishes a normal melee attack. |
| Strange Hand | 13 / 31 / 35 | Full face: Failure performs Basic Action targeting attacker; critical wound permits 1 survival for +1 permanent strength; persistent injury Lost Hand remains in play and affects some AI cards. The page explains the optional payment and replacement of normal AI actions. |
| Clever Ploy | 14 / 32 / 36 | Full face: Trap, attacker doomed, Basic Action targeting attacker, no survival until resolved. Reminder text covers ending attacks, standing a knocked-down monster, and reshuffling all hit locations including the trap. |
| Ground Fighting | 44 / 67 / 71 | Full pictured face and spatial zone, with adjacent explanation: no AI draws; spend activation in the zone to trigger a Basic Action before the activation resolves, with +2 speed and +1 damage; discard on a wound. The diagram remains the source for exact spaces. |

Supporting images inspected: revised 52 (printed 75, original 79) for Traps, Doomed, and Impervious; revised 53 (printed 76, original 80) for critical-wound eligibility, cancellation of reactions, and persistent-injury handling. Revised 44 explains matching persistent-injury actions with Combo Claw and Strange Hand. The prior physical Combo Claw audit supplies its once-per-lifetime understanding limit; the Strange Hand record links that photo without claiming a new inspection in this phase.

Founding Stone retains the critical-wound boundaries: a location without a critical effect cannot be critically wounded, and Impervious prevents a monster wound while allowing applicable critical effects. Strange Hand retains the distinction between its optional survival reward and the persistent injury that remains after the critical wound. Clever Ploy ends attacks while allowing the survivor's act to continue after resolution, as stated by the general trap rules.

Primary image fingerprints are recorded in `SOURCE_HASHES.md` for comparison with the committed source images. The page-map references above make the evidence reviewable without opening either large PDF.

## Retrieval and interaction changes

Card-name selection now supports explicit gear and hit-location names through record metadata, alongside the existing AI-card titles. When multiple named cards appear, selection uses the first named card, with the longer name winning at the same position. This preserves Combo Claw ahead of the contained name Claw. General combat routing no longer replaces a named card with an adjacent general rule merely because the question mentions strength, a critical wound, or knockdown. This remains lexical source selection, with no claim of unrestricted multi-card reasoning.

Combo Claw's notes now state the reusable persistent-injury rule: with Strange Hand's Lost Hand in play, perform the matching Lost Hand action, ignore normal actions including the attack and extra-draw condition, then discard Combo Claw. The supporting moods record explains why. No special answer keyed to an evaluation question was added.

## Verification

The twelve cases in `QUESTIONS.md` were fixed after reviewing source images and before changing records or retrieval. The baseline selected the expected primary source or unsupported status in 4/12 cases: N06, N10, N11, and N12. After the changes, all twelve match their expected categories in the regression tests. N06 also checks the replacement rule and supporting persistent-injury record. Added neighboring checks cover Impervious, locations without critical effects, and edition 1.6 boundaries.

All 100 Python tests pass. HTTP checks verify the four card sources' revised and printed page mappings, image URLs, JPEG media types, and image signatures. Library checks verify 25 records and 28 reviewed pages in local mode and 25 records in the hosted handler. The full-suite run first exposed the hosted handler test's old count of 22; that expectation was updated to 25. `git diff --check` passes.

These are source-guided development and regression results. No live Sol call or independent accuracy evaluation was performed. UI code and hosting configuration were unchanged. No deployment or push was performed. All edits are in the `rules-v2` worktree; the separate `main` checkout was untouched.

## Next coverage

The next acquisition candidates are readable, edition-attributed faces for Chomp, Terrifying Roar, and the full Enraged card. The rulebook's Enraged illustration is cropped and supports only the existing bounded example. Broader coverage needs verifiable card text and images. Cunning remains an unverified gap, unchanged and excluded from this phase. Fresh questions should test card and general-rule conflicts and multi-card selection before treating development results as evidence of broader accuracy.

# Opening White Lion and early-campaign coverage

24 October 2026. Active checkout: `KDM-Rulemaster-v2`, branch `rules-v2`. Local, uncommitted changes only. No push or deployment. The separate `main` checkout was not modified. Cunning remains an unverified, excluded gap.

## Result

Added eight bounded reviewed records, bringing the app to 33 topics across 36 source pages. Fixed model messaging for linked diagrams and supporting-source mixing between encounters/phases. All 126 automated tests pass. The final HTTP snapshot contains 33 responses: 17 new local cases, seven live Sol versions, and nine local turns from eight affected baseline scenarios. All 24 new source-selection checks and nine affected source/boundary checks matched their expected scope. These are development/regression checks, not independent release acceptance.

The original 81 baseline files are byte-preserved. Their aggregate SHA-256 before and after both answered runs is `cb83fceb0887be0f9bf7a995fc071fa87653a81225b769330719cb31108e2e0d`. Historical grades and first responses were not rewritten.

## Source review

Evidence comes from the project's supplied 1.5 rulebook page images. Every source below was visually inspected during this task; all are below 1 MB. No PDF, large physical photo, wiki draft, or unverified online card was used for new transcription. [Source fingerprints](source-hashes.tsv) identify the 11 reviewed images used by the batch. Summaries preserve rule order and scope; they are not full-page transcriptions or independent human verification.

| New unit | Reviewed image evidence and mechanical scope |
| --- | --- |
| Empty AI decks and killing wound | [Revised 15, book 33, original 37](../../kdm-assistant/public/pages/15.jpg): reshuffle an existing discard, Basic Action with both piles empty, and the additional killing wound. This unit carries no encounter-specific rewards. |
| White Lion Basic Action / Monster Reference | [31 / 51 / 55](../../kdm-assistant/public/pages/31.jpg) shows both card faces: closest survivor in field of view, no target Sniff, and Speed 2 / Accuracy 2+ / Damage 1. The reference distinguishes First Story movement 6/toughness 6 from standard level 1 movement 6/toughness 8. [46 / 69 / 73](../../kdm-assistant/public/pages/46.jpg) supports movement limits; [120 / 179 / 183](../../kdm-assistant/public/pages/120.jpg) provides readable Sniff text. |
| First Story victory | [15 / 33 / 37](../../kdm-assistant/public/pages/15.jpg): living survivors' Hunt XP, four resources from each deck, critical-wound resources in addition, and the First Story exception returning dead survivors' gear/resources. |
| First-settlement return/timeline | [16 / 34 / 38](../../kdm-assistant/public/pages/16.jpg), continuing to [17 / 35 / 39](../../kdm-assistant/public/pages/17.jpg): return, healing, survival cap, endeavors, timeline, First Day before Returning Survivors, death count, and milestones. Detailed First Day, Language, Returning Survivors, and principle effects remain unreviewed. |
| First-settlement development/crafting/storage | [17 / 35 / 39](../../kdm-assistant/public/pages/17.jpg), with preceding [16 / 34 / 38](../../kdm-assistant/public/pages/16.jpg): initial locations, payment, crafting, departing gear, and recording/archiving storage. The initial one-endeavor-per-location reading follows the overview's three endeavors for three locations and fewer-endeavors instruction; the Lantern Hoard face itself remains unreviewed. Individual recipes and resource substitutions are not established by this procedure. |
| Hunt setup and progression | [39 / 61 / 65](../../kdm-assistant/public/pages/39.jpg), [40 / 62 / 66](../../kdm-assistant/public/pages/40.jpg), [120 / 179 / 183](../../kdm-assistant/public/pages/120.jpg): E spaces, basic events, starting positions, event-revealer rotation, stacked events, empty spaces, monster arrival, and Starvation exception. The pictured Random Event face and example establish the percentile procedure. Specific numbered events and exceptional story-event effects remain separate sources. |
| Standard level 1 attributes and decks | [120 / 179 / 183](../../kdm-assistant/public/pages/120.jpg), [30 / 50 / 54](../../kdm-assistant/public/pages/30.jpg), [42 / 65 / 69](../../kdm-assistant/public/pages/42.jpg), [31 / 51 / 55](../../kdm-assistant/public/pages/31.jpg): random 7 Basic / 3 Advanced / no Legendary, separate special cards, shuffled monster hit locations, movement 6 and toughness 8. Full eligible-face inventories remain missing. |
| Standard level 1 aftermath | [120 / 179 / 183](../../kdm-assistant/public/pages/120.jpg), [24 / 43 / 47](../../kdm-assistant/public/pages/24.jpg), [31 / 51 / 55](../../kdm-assistant/public/pages/31.jpg): XP, proficiency eligibility, resource rewards, first White Lion victory's Catarium addition, and jewelry loss on defeat. First Story exceptions stay separate. |

The rulebook-pictured card evidence is independent of the dormant online data-card draft. That draft remains outside runtime retrieval. The full physical-set eligible-card inventory and missing Chomp, Terrifying Roar, and Enraged faces remain gaps.

## Diagram and retrieval repair

The [Ground Fighting image](../../kdm-assistant/public/pages/44.jpg) shows the card and Zone of Death. Its reviewed record now states that the linked diagram is available and that exact square coordinates have not been transcribed. Model context includes layout, linked-source availability, and interpretation limits. The request contains text metadata without image pixels. Instructions direct the player to an available diagram, prohibit claiming that listed image is missing, and prohibit inventing untranscribed geometry.

Supporting records now prioritize declared dependencies, require a named card to be mentioned before borrowing it, and exclude conflicting encounter/phase sources unless the question requests them. Shared phase/monster words alone do not qualify an extra reference. Standard deployment explicitly supplies the level 1 deck record. The generic killing-wound mechanic has a separate record so standard fights do not inherit Prologue rewards. First Day's named-source boundary permits a settlement ordering question while retaining the missing-card boundary for instructions/population outcomes.

## Saved runs and review

The first answered run remains at this directory's root: 31 responses, six actual Sol calls, 5,644 input and 840 output tokens. Its source selections passed, but supporting-source review found Prologue/standard mixing and an omitted deck dependency. Those findings prompted the general repair and separate final run. A setup error before any API request is preserved as `setup-failure-metadata.json`; the harness initialization was corrected before the first answered run.

[Final results](final/run-summary.json): 33 responses, seven actual Sol calls, 5,682 input and 1,041 output tokens. Across both answered runs: 13 successful calls and 13,207 tokens. No API fallback, automatic paid retry, or key copy occurred. The user-authorized key file was read in memory. Temporary servers and history databases were closed.

The final wrapper adds N17 to the base protocol. The literal `protocol` sentence in final metadata still describes the base 16-case/six-call list; actual final counts are 17 local cases and seven Sol cases, as recorded in the final summary and response files. Metadata was preserved rather than rewritten.

| Final live case | Answer review |
| --- | --- |
| N02 | Correct First Story rewards, living-survivor XP, and dead-survivor gear exception. |
| N05 | Correct first-settlement order, survival/healing/endeavors, and explicit missing detailed event sources. |
| N06 | Correct crafting/storage procedure and a request for the specific recipe source; no invented recipe price. |
| N08 | Correct standard level 1 rewards, conditional proficiency, and first-victory Catarium. |
| N09 | Correct activation trigger, +2 speed/+1 damage, discard condition, and available linked diagram. |
| N10 | Linked diagram identified; exact three-squares-behind geometry left unresolved. |
| N17 | Correct standard deployment plus random 7 Basic/3 Advanced deck; no Prologue fixed-deck substitution. |

Affected baseline local checks: Q05 selects killing wound; Q06 selects First Story rewards; Q13 retains Ground Fighting; Q20 selects First Story setup then standard deployment with the deck dependency; Q21 selects first-settlement ordering; Q22 retains the missing First Day outcomes; Q24 selects crafting procedure; Q27 selects hunt procedure. All nine decisions match scope. This does not regrade or replace the original baseline.

Each run checked 20 distinct local citation images through HTTP with successful JPEG responses, including the actual Ground Fighting diagram. External Fandom content was not fetched or reverified. No browser/device layout or deployment verification was performed. Automated tests cover source boundaries, exact card fields, neighboring roll/event cases, phase separation, image metadata, local/hosted context, and citation mapping. `git diff --check` passes.

## Remaining work

Required missing evidence includes Chomp, Terrifying Roar, full Enraged, eligible AI/hit-location inventories and remaining faces, First Day, Language, full Returning Survivors, initial location faces/recipes, repeating settlement rules, Tall Grass, and remaining injury/Brain Trauma units. Unfamiliar combined-card and phase-change cases remain necessary before release. No release checklist row is closed by this batch alone.

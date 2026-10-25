# OCR method benchmark: provisional card selection

Selected 3 October 2026. This is a metadata-only screening set for testing whether a transcription method transfers across card families. It is separate from `KDM_OCR_Queue.md`, which prioritizes early-game source ingestion. No image from this set was opened, extracted, or OCR-scanned for this selection.

## Selection rule

Source: Simulator `core-expansion-win_0.1.298` Addressables `catalog.json`, SHA-256 `007DE4BD5530237D577C6DBAB433F016FFE588E60F04DC43826EA9D5EB4F6E42`. Its `m_InternalIds` contain 897 distinct `.png` or `.jpg` paths under `Import/Cards/`. The twelve strata below contain 357 provisional candidates after filtering.

Use the relative path after `Import/Cards/`. Exclude obvious backs, `Materials`, the unclassified `FRONT` files, `-2.png` variants, `Gear/Starting Gear/starting-gear.png`, and the three White Lion AI cards already used as OCR diagnostics: Claw, Size Up, and Grasp. Use nested monster AI folders rather than the overlapping separate White Lion deck folder. These filename rules identify candidates; they do not verify image content or edition.

For each stratum, sort candidates by the hexadecimal SHA-256 digest of `kdm-v2-ocr-pilot-2026-10-03|` followed by the relative path. The first path is the development example; the second is the holdout. Keep holdout images and text unseen while choosing or tuning a method. If an image proves to be a back, duplicate, wrong edition, or unreadable, take the next ranked eligible path from that same stratum and record the replacement. Starting gear has only two eligible named cards, so that stratum may remain incomplete if either fails review.

This 24-card set is a screening pilot. A clean result would justify a larger held-out test; it would not establish production accuracy by itself.

## Selected paths

| Stratum | Role | Catalog path relative to `Import/Cards/` |
| --- | --- | --- |
| AI, White Lion | Development | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0014_15---A---Blood-Thirsty.png` |
| AI, White Lion | Holdout | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0006_07---B---Vicious-Claw-15U.png` |
| AI, other monster | Development | `Screaming Antelope/AI - Screaming Antelope/19---A---infested.png` |
| AI, other monster | Holdout | `Screaming Antelope/AI - Screaming Antelope/20---A---ravenous.png` |
| Hit location, White Lion | Development | `White Lion/HL - White Lion/04---Beast's-Temple.png` |
| Hit location, White Lion | Holdout | `White Lion/HL - White Lion/10---Beast's-Elbow.png` |
| Hit location, other monster | Development | `Screaming Antelope/HL - Screaming Antelope/20---Furry-Tail.png` |
| Hit location, other monster | Holdout | `Screaming Antelope/HL - Screaming Antelope/07---Restless-Rump.png` |
| Gear, starting | Development | `Gear/Starting Gear/07---Founding-Stone---1.png` |
| Gear, starting | Holdout | `Gear/Starting Gear/01---Cloth---1.png` |
| Gear, other | Development | `Gear/Skinnery/01---Rawhide-Boots---1.png` |
| Gear, other | Holdout | `Gear/White Lion/16---Cat-Gut-Bow-1.png` |
| Resource, basic | Development | `Basic Resources/20---WILD.png` |
| Resource, basic | Holdout | `Basic Resources/07---hide.png` |
| Resource, other | Development | `Phoenix/R - Phoenix/05---Small-Feathers.png` |
| Resource, other | Holdout | `White Lion/R - White Lion/01---Great-Cat-Bones.png` |
| Event, settlement | Development | `Settlment Events/First-Day.png` |
| Event, settlement | Holdout | `Settlment Events/Nickname.png` |
| Event, hunt | Development | `White Lion/H - White Lion/04---Sea-of-Golden-Grass.png` |
| Event, hunt | Holdout | `Screaming Antelope/H - Screaming Antelope/07---Carpet-of-Ticks.png` |
| Innovation, basic | Development | `Innovation Cards/02---basic---paint.png` |
| Innovation, basic | Holdout | `Innovation Cards/01---Basic---Language.png` |
| Innovation, other | Development | `Innovation Cards/40---Ultimate-Weapon.png` |
| Innovation, other | Holdout | `Innovation Cards/36---P---Birth---Protect-the-Young 1.png` |

## Gate before a transcription run

Obtain accessible card-front images, confirm their edition and role, and compare decoded pixel hashes within the selected set. The core bundle remains encrypted, so catalog paths alone cannot complete this gate. Keep the existing Claw, Size Up, and Grasp trials as diagnostics outside the holdout set.

When images are available, compare methods on the development cards, freeze the method, and then evaluate holdouts. Score exact gameplay-critical fields, including numbers, dice notation, conditions, triggers, icons, and reading order. Record unflagged errors and reviewer time. Any unflagged gameplay-critical error fails the source-ingestion gate for that method.

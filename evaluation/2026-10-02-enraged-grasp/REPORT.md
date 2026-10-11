# Enraged and Grasp source audit

2 October 2026. This audit covers a level 1 White Lion with Enraged in play and a Grasp attack that deals damage. It uses the supplied edition 1.5 scan and the extracted Grasp image. No app rule record, OCR output, or code changed in this audit.

## Verified sources

| Source | Relevant evidence |
| --- | --- |
| Focused rulebook PDF page 11, original scan page 33, printed page 29 | The First Story explains that Enraged gives the White Lion a +1 damage token, increasing damage from attack profiles by 1. The Enraged card illustration is partly covered, so this page is not a full card transcription. |
| Focused PDF page 30, original page 54, printed page 50 | Monster damage applies to attack profiles. Grab is an example of damage outside an attack profile. |
| Focused PDF page 47, original page 74, printed page 70 | Attack-profile damage is modified by the monster's damage attribute and damage tokens. Each hit is resolved at one hit location. |
| Focused PDF page 48, original page 75, printed page 71 | After Damage effects apply after attack damage. The page names Grasp's Grab as damage outside an attack profile. That damage is unaffected by monster attributes or tokens and cannot be dodged. |
| `D:\Documents\KDM\White Lion AI comparison\Monster folder\ai-lion-deck-v5-final_0009_10---B---Grasp.png` | Grasp has Speed 1, Accuracy 2+, Damage 1. Its After Damage effect says the target suffers Grab. Grab deals 1 damage per monster level. |

## Supported level 1 ruling

While Enraged is in play, a Grasp hit has 2 attack-profile damage: its printed 1 plus the +1 damage token. After that attack deals damage, Grasp's After Damage effect causes Grab. At monster level 1, Grab deals 1 separate damage. The Enraged token does not increase that Grab damage because it occurs outside the attack profile.

This conclusion is limited to the stated conditions. The complete Enraged card image is still needed to verify its full token scaling, discard condition, and wording for other monster levels. The PDF's Enraged illustration is partly hidden. The existing Grasp image was read visually; no OCR was needed for this audit.

## Bounded app test to build next

Use this as a multi-source question: "A level 1 White Lion has Enraged in play. Grasp hits and deals damage. Does the bonus affect the attack, Grab, or both?" A supported answer should give 2 damage for the attack profile and 1 separate damage for Grab, explain why the token stops at the profile, and cite both the Grasp card and printed rulebook pages 29, 70, and 71. Keep the card effect and rulebook mechanics as separate retrieved sources. Do not rely on a hard-coded Grasp exception.

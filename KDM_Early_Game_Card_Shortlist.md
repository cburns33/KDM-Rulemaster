# Early game card asset shortlist

Updated 2 October 2026. This is a metadata selection from the Simulator's `core-expansion-win_0.1.298` Addressables catalog. Paths below are relative to `Import/Cards/`. A filename identifies an image asset; it does not establish card text, deck composition, copy count, or when the card enters play. No images were extracted for this shortlist and no OCR was run.

## What the White Lion folders show

`White Lion/AI - White Lion/` has 28 PNG paths. `AI White Lion Deck/` has 23. Twenty-two filenames occur in both folders. The monster folder alone has the `-2` files for Claw, Size Up, and Grasp, plus `00---White-Lion-AI-Card-Back.png` and the `07---white-lion-FRONT---15U.png` and `07---white-lion-BACK---15U.png` pair. The deck folder alone has `AI-White-LIon-Back.png`. Grasp, Claw, and Size Up were compared across folders by decoded pixel hash and by visual inspection; each matched pair has identical pixels. No other pairs have been image-checked.

The matching filenames suggest two asset groupings with shared card faces. The `-2` names may represent repeat copies, but that needs an image check and deck evidence.

## First extraction and source checks

| Purpose | Catalog path |
| --- | --- |
| Grasp ruling | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0009_10---B---Grasp.png` |
| Enraged ruling | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0018_19---A---Enraged.png` |
| Related White Lion rule | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0019_20---A---Ground-Fighting.png` |
| Hit location context | `White Lion/HL - White Lion/19---Fuzzy-Groin.png` |
| Starting gear | `Gear/Starting Gear/01---Cloth---1.png` |
| Starting gear | `Gear/Starting Gear/07---Founding-Stone---1.png` |
| Basic resources | `Basic Resources/01---bone.png` |
| Basic resources | `Basic Resources/07---hide.png` |
| Basic resources | `Basic Resources/16---organ.png` |
| White Lion resource | `White Lion/R - White Lion/07---White-Fur.png` |
| First settlement candidate | `Settlment Events/First-Day.png` |
| First settlement candidate | `Settlement Locations/06---Lantern-Hoard-1.5.png` |
| First settlement candidate | `Innovation Cards/01---Basic---Language.png` |

Grasp, Claw, and Size Up base images are already present in `D:\Documents\KDM\White Lion AI comparison`. Reuse those samples for the repeat-copy check.

## Small duplicate check

Compare the three `-2` paths against their base cards in the monster folder:

- `White Lion/AI - White Lion/ai-lion-deck-v5-final_0001_02---B---Claw-2.png`
- `White Lion/AI - White Lion/ai-lion-deck-v5-final_0005_06---B---Size-Up-2.png`
- `White Lion/AI - White Lion/ai-lion-deck-v5-final_0010_11---B---Grasp-2.png`

Compare Enraged across the two folders and compare the distinct AI backs:

- `AI White Lion Deck/ai-lion-deck-v5-final_0018_19---A---Enraged.png`
- `White Lion/AI - White Lion/00---White-Lion-AI-Card-Back.png`
- `AI White Lion Deck/AI-White-LIon-Back.png`

The `07---white-lion-FRONT---15U.png` and matching back remain unclassified. The core expansion bundle is encrypted, and a bounded scan of the installed game's managed assemblies, executable, and UnityPlayer.dll found no usable key. The listed duplicate checks have not been extracted or hashed. Before adding text to the source library, compare any OCR output with the card images and the verified rulebook source.

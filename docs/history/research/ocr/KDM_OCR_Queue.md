# Early-game OCR queue

Updated 3 October 2026. This queue turns `KDM_Early_Game_Card_Shortlist.md` into an evidence-based first pass. Paths are relative to the Simulator core catalog's `Import/Cards/`. **Queue** means a candidate for OCR after extraction and image deduplication. **Skip** means OCR would repeat a confirmed identical image. **Hold** means the image, relevance, or existing transcription needs review. Three existing samples have had checked OCR trials; no batch OCR or new extraction has started.

The separate method-screening sample and its fixed selection rule are in `KDM_OCR_Benchmark_Selection.md`. That sample includes card families beyond the early-game ingestion queue.

## Completed trials

`White Lion/AI - White Lion/ai-lion-deck-v5-final_0004_05---B---Size-Up.png` was OCR-scanned and checked against the image. The corrected text and OCR errors are in `evaluation/2026-10-02-size-up-ocr/REPORT.md`. Its separate-deck duplicate remains a confirmed OCR skip. No app rule record was added from this trial.

`White Lion/AI - White Lion/ai-lion-deck-v5-final_0000_01---B---Claw.png` and `White Lion/AI - White Lion/ai-lion-deck-v5-final_0009_10---B---Grasp.png` were also OCR-scanned and checked. Their corrected text and errors are in `evaluation/2026-10-02-claw-grasp-ocr/REPORT.md`. Both OCR runs missed the profile's Speed and Damage values. Their separate-deck duplicates remain confirmed OCR skips. No app rule records were added from these trials.

## Queue after image access and deduplication

| Asset path | Reason |
| --- | --- |
| `White Lion/AI - White Lion/ai-lion-deck-v5-final_0018_19---A---Enraged.png` | Full card text is needed to extend the current level 1 ruling. |
| `White Lion/AI - White Lion/ai-lion-deck-v5-final_0019_20---A---Ground-Fighting.png` | Card text can be checked against the reviewed rulebook example. |
| `White Lion/HL - White Lion/19---Fuzzy-Groin.png` | Verify the card-specific priority effect. |
| `Gear/Starting Gear/01---Cloth---1.png` | Starting gear. |
| `Gear/Starting Gear/07---Founding-Stone---1.png` | Starting gear. |
| `Basic Resources/01---bone.png` | Basic resource. |
| `Basic Resources/07---hide.png` | Basic resource. |
| `Basic Resources/16---organ.png` | Basic resource. |
| `White Lion/R - White Lion/07---White-Fur.png` | White Lion resource. |

The three existing sample images can be used without extracting them again. Other queued assets remain blocked by the encrypted core bundle. Before OCR, compare decoded pixels among any newly available candidate images and read the card faces to confirm identity and edition.

## Confirmed OCR skips

These separate-deck images have the same decoded pixels as the matching monster-folder samples. Keep the monster-folder path as the canonical reference for this queue.

| Skip this path | Matching canonical path |
| --- | --- |
| `AI White Lion Deck/ai-lion-deck-v5-final_0000_01---B---Claw.png` | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0000_01---B---Claw.png` |
| `AI White Lion Deck/ai-lion-deck-v5-final_0004_05---B---Size-Up.png` | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0004_05---B---Size-Up.png` |
| `AI White Lion Deck/ai-lion-deck-v5-final_0009_10---B---Grasp.png` | `White Lion/AI - White Lion/ai-lion-deck-v5-final_0009_10---B---Grasp.png` |

This is an OCR decision about image content. It does not establish the number of copies in the playable AI deck.

## Hold for evidence or scope review

| Asset or group | Reason |
| --- | --- |
| `White Lion/AI - White Lion/ai-lion-deck-v5-final_0001_02---B---Claw-2.png` | Compare decoded pixels with base Claw; `-2` alone does not prove identical art. |
| `White Lion/AI - White Lion/ai-lion-deck-v5-final_0005_06---B---Size-Up-2.png` | Compare decoded pixels with base Size Up. |
| `White Lion/AI - White Lion/ai-lion-deck-v5-final_0010_11---B---Grasp-2.png` | Compare decoded pixels with base Grasp. |
| `AI White Lion Deck/ai-lion-deck-v5-final_0018_19---A---Enraged.png` | Compare decoded pixels with the monster-folder Enraged image before selecting one for OCR. |
| `White Lion/AI - White Lion/00---White-Lion-AI-Card-Back.png` and `AI White Lion Deck/AI-White-LIon-Back.png` | Inspect both backs before treating them as text-free OCR skips. |
| `White Lion/AI - White Lion/07---white-lion-FRONT---15U.png` and `White Lion/AI - White Lion/07---white-lion-BACK---15U.png` | Content and card role are unclassified. |
| `Settlment Events/First-Day.png`, `Settlement Locations/06---Lantern-Hoard-1.5.png`, and `Innovation Cards/01---Basic---Language.png` | First-settlement candidates; confirm campaign priority before the first OCR pass. |
| Other matching White Lion AI filenames across the two folders | Filename overlap is known; pixel identity has not been checked. Keep them out of the skip list. |

## Gate for moving an item

Move **hold** to **skip** only after an identical pixel comparison or a documented decision that its text is already covered by a verified source. Move **queue** to OCR only when its image is available, its face and edition are confirmed, and duplicate checks are complete. Compare OCR text with the image before adding it to the app's source library.

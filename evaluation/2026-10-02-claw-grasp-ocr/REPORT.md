# Claw and Grasp OCR-quality trials

2 October 2026. Sources are the existing monster-folder samples in `D:\Documents\KDM\White Lion AI comparison`. Their separate-deck counterparts have identical decoded pixels, so those images were not scanned again. These two trials did not extract assets or add app rule records. Card edition remains unverified from these images.

## Claw

Source: `ai-lion-deck-v5-final_0000_01---B---Claw.png`

Image-checked transcription:

- Pick Target: closest threat, facing, in range; then closest threat, in field of view; if no target, sniff.
- Move & Attack Target: Speed 2, Accuracy 2+, Damage 1. The Trigger field is blank.

The OCR returned 12 text segments. Its raw text, in detected order, was:

```text
Claw | Pick Target | . closest threat, facing, in range | : closest threat, in field of view | : no target: sniff | Move | & Attack Target | Accuracy | Speed | Damage | Trigger | 2+
```

The OCR found the target list and Accuracy 2+, but it omitted Speed 2 and Damage 1. It also split the action heading and returned profile labels out of their visual column order.

## Grasp

Source: `ai-lion-deck-v5-final_0009_10---B---Grasp.png`

Image-checked transcription:

- Pick Target: closest knocked down survivor, in range; then closest survivor, in range; if no target, sniff.
- Move & Attack Target: Speed 1, Accuracy 2+, Damage 1, with an After Damage trigger.
- After Damage effect: The White Lion isolates its prey. Full move the White Lion away from all threats. Target suffers Grab.
- Grab: Place target knocked down in front of the monster. Target suffers 1 damage per monster level.

The OCR returned 19 text segments. Its raw text, in detected order, was:

```text
Grasp | Pick Target | . closest knocked down survivor, in range | . closest survivor, in range | : no target: sniff | Move | & Attack Target | Speed | Accuracy | Damage | Trigger | 2+ | *AfterDamage | The White Lion isolates its prey. Full | movethewhiteLionawayfromall | threats.Target suffers Grab. | Grab: Place target knocked down in | front of the monster. Target suffers 1 | damage per monster level.
```

The OCR omitted Speed 1 and Damage 1, merged `After Damage`, and joined words in the movement instruction. It did capture the Grab damage line. The symbol beside the effect must be checked visually to associate that text with the After Damage trigger.

## Pipeline implication

These runs show a repeatable risk for this card layout: OCR can capture narrative lines while losing numeric profile cells and trigger structure. A future scan pipeline should preserve image coordinates, inspect every profile cell and trigger, and compare the assembled text with the card image before adding a source record. The two cases are tests of that general validation requirement. Enraged and Ground Fighting remain queued because their images are unavailable outside the encrypted bundle.

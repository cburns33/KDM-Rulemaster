# OCR benchmark source audit, 2026-10-03

## Scope

This audit concerns the 24 provisional development and holdout paths in `KDM_OCR_Benchmark_Selection.md`. It checks access to card-front images. It does not validate the selected cards, transcribe them, or run OCR.

## Findings

- The local KDM workspace contains 428 PNG, JPG, JPEG, or WebP files. Most are three copies of the same 138 rulebook page images. The six comparison files are the three White Lion AI images in each of two folders. None of the 24 selected catalog filenames has an exact local image-file match.
- A separate search for selected card names also found no local card-front image. This name search covered representative titles, while the exact-filename check covered all 24 selections.
- The official [Kingdom Death downloads page](https://kingdomdeath.com/rules/downloads) lists record sheets and a few other assets. It does not list a core-game card-front archive.
- The official [Kingdom Death: Monster 1.6 product page](https://shop.kingdomdeath.com/products/kingdom-death-monster-1-5) includes product images and a component list. Its inspected images did not provide the selected full card fronts.
- A community card database exists at [Vibrant Lantern](https://vibrantlantern.com/carddb/search/), but it is a secondary source. Its page was unavailable during this audit. Community text or imagery would need edition and card-front checks before use as benchmark input or ground truth.

## Decision gate

Keep the 24 catalog paths as a metadata-only sample. Do not score OCR against filenames, community transcriptions, or product photos. The next useful input is card-front captures from the licensed Simulator, or clear photographs/scans of the matching physical cards. For each image, record the catalog path or physical edition, front/back status, capture source, dimensions, and file hash. If a selected card is unavailable or is not a front, use the next ranked candidate in its stratum as specified in the selection document.

Once images are available, validate a small development subset across different families before opening the holdout images. The three White Lion diagnostic cards remain outside this benchmark.

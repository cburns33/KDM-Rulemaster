# Limited wiki card-text extraction, 5 October 2026

## Scope

Extracted the three wiki revisions already staged locally: Maul (28126), Combo Claw (28091), and White Lion Data Card (28563). This run made no new wiki requests. The draft files are in the ignored `kdm-assistant/data/wiki-drafts/` folder and remain outside the app's reviewed answer records.

## Result

| Page | Extracted card information | Comparison with supplied photo |
| --- | --- | --- |
| Maul | Ordered targets; Speed 2, Accuracy 2+, Damage 3; After Damage trigger; Bleed and Bash effects. | Matches the photographed face. The wiki identifies it as an Advanced card. |
| Combo Claw | Ordered targets; Speed 2, Accuracy 4+, Damage 1; conditional AI draw; Lost Hand persistent injury. | Matches the photographed face. The wiki identifies it as a Basic card. |
| White Lion Data Card | First Story and levels 1-3 deck counts and attributes; Sniff; a separate Basic Action section. | The photographed face matches the level rows and Sniff. The Basic Action section is additional wiki content that the supplied photo does not show. |

The parser keeps headings, target order, tables, flow markers, merged table-cell width, wiki links, template names, categories, source URL, and revision ID. It leaves template icons as labeled placeholders and linked rules as references. This preserves missing-context signals such as Maul's linked Grab term.

## Limits

These are extraction drafts, not rulings or complete card-front certifications. The parser does not expand linked definitions, resolve every template, establish 1.5 compatibility for other cards, or prove completeness across wiki pages. No draft is loaded into answer retrieval. The White Lion Basic Action needs a separate source check before it is treated as part of the photographed card face.

Next test: produce a read-only answer preview for Maul from its existing draft. Show the source URL and revision, and identify Grab as a linked definition missing from this local source set. This will test answer usefulness without new wiki requests, image extraction, or OCR.

# Lantern Archive

A browser companion for the supplied Kingdom Death: Monster 1.5 scan. It runs locally and includes a Vercel deployment path.

## Iteration 2 mission

This branch aims to answer unseen play questions from verified card and rulebook evidence, with source citations and clear limits when coverage is missing. Example rulings are tests of general retrieval and reasoning behavior. They are not templates for case-specific answer routing. See `../ITERATION_2.md` for the mission, evaluation standard, and worktree boundary. This branch has not been cleared for hosted deployment.

## Open the app

Double-click `Start.cmd` in this folder. It opens http://127.0.0.1:8765 in your browser. Python 3.10 or newer is required and is already available on this computer. Local lookup needs no package installation, account, API key, or internet connection. Optional Sol explanations use the configured OpenAI API key and an internet connection.

If the app is already running, the launcher opens that instance. When the launcher starts a new server, leave its console open during use and press Ctrl+C in that console to stop it. Closing a browser tab does not stop the server. Your conversations survive restarts.

Ask questions in the main view. Use the menu button for conversation history and Sources for page browsing, reviewed-topic search, the Hands of Heat resolver, and correction notes. Clicking an answer citation opens its page in Sources. Answer settings controls the optional Sol explanation and shows the current review coverage.

## Invite-only Vercel deployment

The Vercel project uses `kdm-assistant` as its Root Directory. Static files and the authorized page images are in `public`; `api/index.py` is a stateless Python Vercel Function. `vercel.json` routes browser API calls to that function and excludes local test files and unused source images from the function bundle.

Import `OPENAI_API_KEY` from the local `.env` into Vercel's Production environment. The key stays in Vercel's server-side environment settings and is never served to a browser. Hosted Sol starts disabled even when the key exists. Enable Vercel Authentication for all deployments in the Vercel project, approve access requests from each friend, then add `KDM_ENABLE_SOL=true` to Vercel's Production environment and redeploy. This avoids building a separate account system and lets you revoke a person's access in Vercel.

The hosted app keeps chat history and follow-up context in each player's browser. Local use retains server-side SQLite history and local correction notes. The hosted correction form is hidden because the serverless deployment has no review database.

## What works

- Local conversation history, stored in `data/history.sqlite3`, plus browser-local hosted history.
- Whole-record text search over 25 reviewed topics, supported by selected rules on 28 source pages, with up to two additional reviewed records selected for compound questions.
- Deterministic resolution of both Hands of Heat tables, including conditions and follow-ons.
- Follow-ups such as “What about 7?”, “Lantern Branding roll 6”, and “We already have Lantern Oven and rolled 6”.
- A form for choosing the table, settlement state, and roll when natural-language parsing is ambiguous.
- All 138 retained page images, with original PDF, revised PDF, and printed-book references.
- Clickable citations that open the relevant rulebook page in Sources, plus layout notes and a local correction-note form.
- Explicit refusal to confirm 1.6 rulings without a verified 1.6 source.

## Current coverage

The next card batch covers Founding Stone, Strange Hand, and Clever Ploy using complete card faces pictured in the supplied 1.5 rulebook. Each record links its page image and supporting rules. Ground Fighting now links its pictured face and Zone of Death diagram. Combo Claw includes the Lost Hand action replacement when Strange Hand is in play. These scan-backed records do not claim a new physical-set photo check. See `../evaluation/2026-10-24-next-card-coverage/REPORT.md` for the source audit and development checks.

Hunt event damage is reviewed on revised PDF page 41 (book 63, original PDF 67), with damage-order and brain-damage support on revised pages 47 and 48. The record covers nonlethal damage, existing injury boxes, carryover, and events that explicitly instruct severe injuries or brain trauma. Injury-table guards preserve general damage questions while refusing results from unreviewed locations.

Combat records include attacker-knockdown cancellation, Encourage timing and restrictions, the wound formula, critical-wound and Impervious exceptions, monster movement, target definitions, and the pictured White Lion Basic Action. Age rolls require a milestone identity before resolution. Only the first milestone table is reviewed; later milestones return a missing-coverage response and retain their identity across short follow-ups. Unspecified or conflicting milestones require clarification. A roll supplied before a clarification is not carried forward; enter the roll again after identifying the milestone.

| Topic | Revised PDF | Printed book | Original PDF |
| --- | ---: | ---: | ---: |
| Hands of Heat | 90 | 125 | 129 |
| Affinities | 28 | 47 | 51 |
| Critical wound rules and examples | 54, 53 | 77, 76 | 81, 80 |
| Create a Survivor | 6 | 24 | 28 |
| First Story: White Lion | 8 | 26 | 30 |
| White Lion: standard deployment | 120 | 179 | 183 |
| Survival actions and timing | 55, 56 | 78, 79 | 82, 83 |
| Monster hits and damage | 47 | 70 | 74 |
| Attack effects and outside damage | 48 | 71 | 75 |
| AI flows, moods, Ground Fighting | 44, 43 | 67, 66 | 71, 70 |
| Priority targeting and exceptions | 45, 46 | 68, 69 | 72, 73 |
| Survivor acts and attack sequence | 50, 51 | 73, 74 | 77, 78 |
| Age: first Hunt XP milestone | 81, 24 | 107, 43 | 111, 47 |
| Severe head injuries | 62 | 86 | 90 |
| White Lion: Claw AI card | 9, 10 | 27, 28 | 31, 32 |
| Monster movement and target definitions | 46, 45 | 69, 68 | 73, 72 |
| Founding Stone gear card and critical-wound limits | 12, 52, 53 | 30, 75, 76 | 34, 79, 80 |
| Strange Hand hit location and Lost Hand | 13, 44, 53 | 31, 67, 76 | 35, 71, 80 |
| Clever Ploy trap and Doomed rules | 14, 52 | 32, 75 | 36, 79 |

The reviewed records are scoped summaries checked by the building assistant against the scan. Review does not imply human verification or complete transcription of every section on a page. First Story and standard White Lion deployment have separate records. The Create a Survivor record covers its first page and flags the continuation. Rules elsewhere remain available as page images but are not indexed as text.

Continuation pages and related references have separate clickable citations. The coverage count includes every source page used by current records. Fuzzy Groin questions link to a community card transcription and the relevant rulebook pages. The Ground Fighting card pictured in the book has been checked.

Local lookup is the default. General questions return relevant reviewed reference text; exact roll outcomes use code. Optional GPT-6 Sol explanations use only the selected reviewed records and may state that the available source is insufficient. A lexical match means “relevant reference,” not proof that the retrieved text answers every part of a question. Follow-up parsing is limited; use the explicit table form for exact resolution. Roll inputs represent a final result including any applicable modifiers; the app does not determine whether a modifier is legal.

## Optional Sol explanations

Sol is available through Answer settings beside the question box. It is off by default. Exact table resolution and clear reviewed lookups stay local, so they never make an API call. The GPT-6 Sol option is configured through a local `.env` file in the project folder and uses the OpenAI Responses API. It sends only the current question and selected reviewed records, returns source-linked answers, and reports when the source does not establish the answer.

GPT-6 Astra is excluded from the app's normal answer path. Reserve it for project work such as interpreting difficult layouts, structuring new source records, and designing tests. It is not a fallback for missing card text or unreviewed rules.

The app owns page citations. Sol's source payload omits original-PDF page metadata, and a separate high-priority instruction tells it to leave page numbers, links, and citation markers out of its prose. Clickable citations retain the revised, printed, and original mappings. Existing saved answers are unchanged. This prompt contract was verified with automated request checks and a one-call live smoke test; it is not a guarantee of compliance on every generated answer.

OpenAI API billing is separate from a ChatGPT or Codex subscription. The app accepts `OPENAI_API_KEY` or `OPENAI_API_SECRET_KEY` from `D:\Documents\KDM\.env`; that file is excluded from version control and never served to the browser. With Sol selected, a source-reference question sends the current question and up to three selected reviewed records to OpenAI. Each request uses low reasoning effort and a 700-token output cap. The full rulebook and unrelated conversation history are excluded.

## Source handling

For one wiki page at a time, run `python wiki_stage.py "Maul"` from this folder, replacing `Maul` with an exact page title. The command uses the MediaWiki API and saves a revision-specific JSON file in `data/wiki-candidates/`. It does not crawl categories, overwrite an existing revision, or promote wiki text into reviewed answer records. The original wikitext stays intact so templates and linked rules can be checked during review. Treat the saved page as an unreviewed candidate for the group's physical 1.5 set; a wiki revision does not establish edition compatibility by itself.

Run `python wiki_extract.py data/wiki-candidates/6042-28126.json` to turn an already staged page into a structured draft in the ignored `data/wiki-drafts/` folder. This local step makes no wiki request. It preserves source revision, ordered card text, table rows, links, and template placeholders. It does not add the draft to the app's reviewed records. The three-sample result and photo comparison are in `../evaluation/2026-10-05-wiki-extraction/REPORT.md`.

The read-only answer preview from the existing Maul draft is in `../evaluation/2026-10-07-maul-preview/REPORT.md`. It shows the source URL and revision and flags the linked Grab definition as missing. The preview was composed for evaluation; it does not add the draft to reviewed answer retrieval. The current [Fandom terms](https://www.fandom.com/terms-of-use) restrict automated extraction and software use without permission, so do not turn the single-page intake into a bulk pull while access and reuse are unresolved. The test's card text came from wiki wikitext; the supplied photos served only as comparison checks. No OCR was used for this wiki-text test.

`wiki_preview.py` is a separate local command for asking GPT-6 Sol about one explicit unreviewed draft, for example `python wiki_preview.py data/wiki-drafts/6042-28126.json "What does Maul instruct?"`. It appends the draft's source URL, revision, unreviewed label, and a missing linked-page notice when the question asks for that definition. It requires a local OpenAI API key and sends the selected draft blocks and question to the Responses API. It does not alter reviewed records, `/api/ask`, or the hosted app. Its request and boundary tests pass. A bounded live evaluation used the existing key in the original checkout without copying it; this worktree itself has no configured key.

Pass `data/wiki-drafts` instead of one JSON file to select among the local drafts by question: `python wiki_preview.py data/wiki-drafts "How many Basic AI cards does a level 2 White Lion use?"`. The command declines missing or ambiguous sources. Its nine fixed selection cases and seven live answers are recorded in `../evaluation/2026-10-07-wiki-selection/`. This local evaluation does not promote wiki drafts into reviewed answers.

The original and revised PDFs remain in their existing locations. The app contains copies of the rendered retained page images in `public/pages`. Local use binds to 127.0.0.1 and loads no remote scripts or fonts. The hosted deployment is access-controlled through Vercel. Opt-in Sol questions are sent to the OpenAI API.

`data/manifest.json` maps all 138 retained pages. `data/source-manifest.json` accounts for all 239 original pages and marks excluded pages. The server computes current review flags and topic titles from the records at startup, so the original stored review flags are not the current coverage inventory. `records.py` and `core_records.py` store structured summaries, layout notes, source continuations, and explicit table ranges. Corrections are saved in the SQLite `corrections` table as pending review and never overwrite verified records automatically.

The browser uses revised PDF page numbers by default. Compact citations show revised PDF and printed-book numbers; `KDM_Rules_Focused_Page_Map.md` has the full revised, original, and printed-book mapping. For example: Hands of Heat is revised PDF 90, book 125, original PDF 129. Unnumbered front matter remains unnumbered. The source filename says 1-6, but the project's inspected scan is treated as 1.5; no 1.6 claims are inferred from the filename.

## Community project decision

The board-game-referee repository was inspected as a candidate. Its documented FastAPI/React, ChromaDB, model API, and chunk retrieval stack is broader than this local reviewed-record prototype needs. This implementation uses Python's standard library and a plain browser UI. No third-party project source code was copied. The source-preview and citation workflow was informed by that project's design. RulesPal supplies a regression case from the previous failed experiment, not ingested rules text.

Reference: https://github.com/ksycz/board-game-referee

## Verification and next steps

Run `python -m unittest discover -v` from this folder. Tests cover roll bands, both table branches, prerequisites, conversation context, page mapping, persistence, unsupported questions, edition checks, server boundaries, community-scenario retrieval, adjacent cases, and continuation citations. The combat regression module checks Age identity and context guards, attacker knockdown, Encourage, movement, wound calculation, and critical-wound evidence. These tests validate retrieval and reviewed content, not open-ended AI reasoning. Browser testing covers the actual local UI.

Next: expand the reviewed source set to other hard layouts, including Age and severe injuries. Play uses edition 1.5. Keep deterministic row selection and source citations outside the Sol path. Check the narrow-screen layout before relying on it during mobile play.

`prepare.py` was used to populate page images from this project's `work/pdf-triage` files and the existing page-map Markdown. It is only needed when regenerating assets in the original workspace. Normal use relies on the bundled data folder.

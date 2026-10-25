# Wiki experiment, dormant

These instructions are preserved from the app guide as of 24 October 2026. They describe the isolated wiki intake and preview experiment, not the active source workflow. No new wiki intake is scheduled. The recorded access/reuse concern remains unresolved; this cleanup does not reassess external terms.

Current source workflow: [Sources](../../../SOURCES.md). Experiment modules and their tests remain in `kdm-assistant/` to preserve imports and saved commands. Existing local drafts remain ignored by Git and outside reviewed retrieval.

Run any saved command from the `kdm-assistant` folder. Statements about missing sources or past test counts below describe their original date.

## Saved experiment instructions

For one wiki page at a time, run `python wiki_stage.py "Maul"` from this folder, replacing `Maul` with an exact page title. The command uses the MediaWiki API and saves a revision-specific JSON file in `data/wiki-candidates/`. It does not crawl categories, overwrite an existing revision, or promote wiki text into reviewed answer records. The original wikitext stays intact so templates and linked rules can be checked during review. Treat the saved page as an unreviewed candidate for the group's physical 1.5 set; a wiki revision does not establish edition compatibility by itself.

Run `python wiki_extract.py data/wiki-candidates/6042-28126.json` to turn an already staged page into a structured draft in the ignored `data/wiki-drafts/` folder. This local step makes no wiki request. It preserves source revision, ordered card text, table rows, links, and template placeholders. It does not add the draft to the app's reviewed records. The three-sample result and photo comparison are in `../../../../evaluation/2026-10-05-wiki-extraction/REPORT.md`.

The read-only answer preview from the existing Maul draft is in `../../../../evaluation/2026-10-07-maul-preview/REPORT.md`. It shows the source URL and revision and flags the linked Grab definition as missing. The preview was composed for evaluation; it does not add the draft to reviewed answer retrieval. The current [Fandom terms](https://www.fandom.com/terms-of-use) restrict automated extraction and software use without permission, so do not turn the single-page intake into a bulk pull while access and reuse are unresolved. The test's card text came from wiki wikitext; the supplied photos served only as comparison checks. No OCR was used for this wiki-text test.

`wiki_preview.py` is a separate local command for asking GPT-6 Sol about one explicit unreviewed draft, for example `python wiki_preview.py data/wiki-drafts/6042-28126.json "What does Maul instruct?"`. It appends the draft's source URL, revision, unreviewed label, and a missing linked-page notice when the question asks for that definition. It requires a local OpenAI API key and sends the selected draft blocks and question to the Responses API. It does not alter reviewed records, `/api/ask`, or the hosted app. Its request and boundary tests pass. A bounded live evaluation used the existing key in the original checkout without copying it; this worktree itself has no configured key.

Pass `data/wiki-drafts` instead of one JSON file to select among the local drafts by question: `python wiki_preview.py data/wiki-drafts "How many Basic AI cards does a level 2 White Lion use?"`. The command declines missing or ambiguous sources. Its nine fixed selection cases and seven live answers are recorded in `../../../../evaluation/2026-10-07-wiki-selection/`. This local evaluation does not promote wiki drafts into reviewed answers.


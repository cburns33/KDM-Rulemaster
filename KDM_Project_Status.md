# KDM rules assistant: project state

Updated 28 September 2026.

Canonical project location: `D:\Documents\KDM`. The live app runs from `kdm-assistant` in that folder. A residual copy may remain in the old Codex outputs folder after the relocation; it is not the active application.

## Deliverables

- `KDM_Rulebook_1.5_Rules_Focused.pdf`: 138 retained pages from the 239-page scan. Table of contents retained.
- `KDM_Rules_Focused_Page_Map.md`: revised PDF, original PDF, and printed-book page map.
- `kdm-assistant/`: working local browser prototype, Lantern Archive. Run `Start.cmd` or open http://127.0.0.1:8765 when running.

## Decisions

- Local lookup is the default. GPT-6 Sol explanations are available when selected for a question. Exact tables and clear reviewed lookups stay local.
- Do not use GPT-6 Astra in the app's normal or fallback answer path. Reserve Astra for project work that benefits from careful source interpretation and test design.
- API billing is separate from ChatGPT and Codex billing. The configured Sol path reads `OPENAI_API_KEY` or `OPENAI_API_SECRET_KEY` from `D:\Documents\KDM\.env`, never serves it to the browser, and sends only a Sol-enabled question plus up to three selected reviewed records. Sol is opt-in per question, uses low reasoning effort, and has a 700-token output cap.
- Revised PDF numbering is the default for user requests. Preserve all three page identifiers in citations.
- Treat the supplied scan as edition 1.5, regardless of its original filename. Edition 1.6 compatibility remains unverified.
- Use a small standalone implementation with Python's standard library and a plain browser frontend. The inspected board-game-referee project informed the source-preview workflow; no community project code was copied.
- Preserve complete rule units and resolve reviewed roll bands in code.
- The obsolete Obsidian session-note instruction is revoked. Do not create Obsidian notes.

## Implemented

Fifteen reviewed topics using selected rules on twenty-one source pages. The original records are joined by the first Age milestone, the severe Head table, and the White Lion Claw AI card shown in the book. Both Hands of Heat subtables retain explicit ranges, rewards, conditions, and follow-ons. All 138 retained pages can be viewed. Conversation history and pending correction notes are stored locally in SQLite. Continuation pages and related records receive clickable source citations. The server computes current review coverage from records at startup.

The browser now opens to a conversation-focused view. In response to feedback that the three-column layout felt crowded, conversation history and rulebook pages were moved into drawers. Clicking a compact citation selects its mapped page and opens Sources. Answer settings contain the opt-in Sol control, API disclosure, coverage count, and edition caveat. The source drawer retains page navigation, reviewed-topic search, Hands of Heat resolution, layout notes, and correction reporting. Answer text renders bold emphasis without showing raw Markdown markers.

## Verification

All 37 automated test methods passed, including the original 23, community scenarios and variations, missing-card evidence, continuation-page mapping, related citations, persisted answers, and the GPT-6 Sol integration. The model checks confirm that Sol is opt-in, runs only for source-reference answers, and falls back to the local reference if the service is unavailable. JavaScript syntax validation passed after the interface change. Browser checks covered the conversation-focused home view, opening and closing both drawers, restoring a saved chat, opening its mapped source page from a citation, and finding the Sol switch in Answer settings. Earlier browser checks confirmed the 12-topic/16-page coverage count, survival citations, the missing-card notice, and a live source-grounded Sol answer for Affinities. The initial build decoded all 138 images.

## Remaining work

Fuzzy Groin's community card transcription is linked to the priority-target record and used for the Ground Fighting interaction. Expand structured coverage to the other Age milestones, severe-injury locations, AI cards, and more layout archetypes. Existing summaries have been checked by the building assistant against page images; they are not complete transcriptions or a claim of independent human verification. Play uses edition 1.5. Sol explanations remain limited to the reviewed records supplied with each question. The narrow-screen layout has not had a separate visual check.

Community prompts and evidence coverage are in `KDM_Community_Test_Questions.md`. The earlier Surge prompt was corrected to activating Tall Grass's hiding effect, rather than moving with Surge. The damage case is an adapted practice scenario from a reference post. These are source-guided regression checks, not a blind comprehension benchmark: search results exposed community replies during collection.

A 14-question local lookup evaluation found five inadequate initial results. Fuzzy Groin paraphrases now route to the card-backed priority record. Source review then added the first Age milestone, the severe Head table, and the Claw card pictured in the rulebook, so all 14 original prompts now have supported answers. The app has 15 reviewed records on 21 source pages, and 39 automated tests pass. The evaluation did not invoke Sol or establish general answer accuracy. Other Age milestones, injury locations, and AI cards still need coverage. Details are in `KDM_Community_Test_Questions.md`.

See `kdm-assistant/README.md` for launch, source coverage, data locations, and test commands. This state note can be used to resume after `/compact` or in a new session.

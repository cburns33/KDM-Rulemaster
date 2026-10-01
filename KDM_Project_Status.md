# KDM rules assistant: project state

Updated 30 September 2026.

Canonical project location: `D:\Documents\KDM\KDM-Rulemaster`. The live app runs from `kdm-assistant` in that folder. The preceding non-Git working folder is preserved at `D:\Documents\KDM\archive-pre-git-source` as a recoverable archive.

## Current snapshot

Lantern Archive has 17 reviewed topics supported by 23 source pages from the supplied edition 1.5 scan. It serves local lookup by default, plus opt-in GPT-6 Sol explanations grounded only in selected reviewed records. The local app is healthy on port 8765. A Vercel hosting conversion is ready for the linked project, with the first production check pending deployment. All 69 automated tests pass.

The September 30 fixes cover hunt-event damage, attacker knockdown, Encourage timing, Age-milestone identity and follow-ups, monster movement and target definitions, wound calculation, critical wounds, and mapped model citations. Four earlier targeted audits and their regression retest are preserved in `evaluation/2026-09-30-*`. The latest citation smoke test used one Sol call and returned no page references in generated prose.

Primary remaining coverage work: later Age milestones, severe injuries outside Head, more AI cards, and fresh holdouts with new wording. Rule coverage remains limited to the reviewed records; the assistant does not claim complete rulebook coverage or edition 1.6 compatibility.

## Deliverables

- `KDM_Rulebook_1.5_Rules_Focused.pdf`: 138 retained pages from the 239-page scan. Table of contents retained.
- `KDM_Rules_Focused_Page_Map.md`: revised PDF, original PDF, and printed-book page map.
- `kdm-assistant/`: Lantern Archive for local use and Vercel hosting. Run `Start.cmd` or open http://127.0.0.1:8765 when running locally.

## Decisions

- Local lookup is the default. GPT-6 Sol explanations are available when selected for a question. Exact tables and clear reviewed lookups stay local.
- Do not use GPT-6 Astra in the app's normal or fallback answer path. Reserve Astra for project work that benefits from careful source interpretation and test design.
- API billing is separate from ChatGPT and Codex billing. The configured Sol path reads `OPENAI_API_KEY` or `OPENAI_API_SECRET_KEY` from `D:\Documents\KDM\KDM-Rulemaster\.env`, never serves it to the browser, and sends only a Sol-enabled question plus up to three selected reviewed records. Sol is opt-in per question, uses low reasoning effort, and has a 700-token output cap.
- Revised PDF numbering is the default for user requests. Preserve all three page identifiers in citations.
- Treat the supplied scan as edition 1.5, regardless of its original filename. Edition 1.6 compatibility remains unverified.
- Use a small standalone implementation with Python's standard library and a plain browser frontend. The inspected board-game-referee project informed the source-preview workflow; no community project code was copied.
- Preserve complete rule units and resolve reviewed roll bands in code.
- The obsolete Obsidian session-note instruction is revoked. Do not create Obsidian notes.
- Host the friend-group deployment on Vercel with Vercel Authentication, rather than storing player passwords in the app. The owner approves only named friends with Vercel accounts.
- The hosted function is stateless. Browser-local storage holds hosted chat history and follow-up context; local SQLite history and correction reports remain local-only features.
- Hosted Sol is disabled by default, even when `OPENAI_API_KEY` is present. Enable `KDM_ENABLE_SOL=true` only after Vercel Authentication protects production.

## Implemented

Seventeen reviewed topics using selected rules on twenty-three source pages. The original records are joined by the first Age milestone, the severe Head table, the White Lion Claw AI card, attacker-knockdown, Encourage, critical-wound, and monster-movement rules. Both Hands of Heat subtables retain explicit ranges, rewards, conditions, and follow-ons. All 138 retained pages can be viewed. Conversation history and pending correction notes are stored locally in SQLite. Continuation pages and related records receive clickable source citations. The server computes current review coverage from records at startup. Authorized page images are now static deployment assets in `kdm-assistant/public/pages`.

The browser now opens to a conversation-focused view. In response to feedback that the three-column layout felt crowded, conversation history and rulebook pages were moved into drawers. Clicking a compact citation selects its mapped page and opens Sources. Answer settings contain the opt-in Sol control, API disclosure, coverage count, and edition caveat. The source drawer retains page navigation, reviewed-topic search, Hands of Heat resolution, layout notes, and correction reporting. Answer text renders bold emphasis without showing raw Markdown markers.

## Verification

All 69 automated test methods pass, including the original interface and persistence coverage, rule-table boundaries, injury and Age guards, saved follow-up scope, model payload and citation contracts, related sources, and local HTTP boundaries. The hosted API tests cover stateless browser-supplied follow-up context, Sol opt-in behavior, and Vercel rewrite routing. Local static-asset checks cover the moved browser UI and source images. Targeted live checks cover source-grounded Sol answers for the added combat rules and the page-reference mitigation. The model checks confirm that Sol is opt-in, runs only for source-reference answers, and falls back to the local reference if the service is unavailable. JavaScript syntax validation and the earlier browser checks covered the conversation-focused home view, drawers, saved chats, mapped source pages, and Answer settings. The initial build decoded all 138 images.

## Remaining work

Fuzzy Groin's community card transcription is linked to the priority-target record and used for the Ground Fighting interaction. Expand structured coverage to the other Age milestones, severe-injury locations, AI cards, and more layout archetypes. Existing summaries have been checked by the building assistant against page images; they are not complete transcriptions or a claim of independent human verification. Play uses edition 1.5. Sol explanations remain limited to the reviewed records supplied with each question. The narrow-screen layout has not had a separate visual check. After the Vercel push, enable Vercel Authentication, approve each friend, and run a live production smoke test.

Community prompts and evidence coverage are in `KDM_Community_Test_Questions.md`. The earlier Surge prompt was corrected to activating Tall Grass's hiding effect, rather than moving with Surge. The damage case is an adapted practice scenario from a reference post. These are source-guided regression checks, not a blind comprehension benchmark: search results exposed community replies during collection.

A 14-question local lookup evaluation found five inadequate initial results. Fuzzy Groin paraphrases now route to the card-backed priority record. Source review then added the first Age milestone, the severe Head table, and the Claw card pictured in the rulebook, so all 14 original prompts now have supported answers. The app has 15 reviewed records on 21 source pages, and 39 automated tests pass. The evaluation did not invoke Sol or establish general answer accuracy. Other Age milestones, injury locations, and AI cards still need coverage. Details are in `KDM_Community_Test_Questions.md`.

See `kdm-assistant/README.md` for launch, source coverage, data locations, and test commands. This state note can be used to resume after `/compact` or in a new session.

## Holdout evaluation, 29 September 2026

Evaluated baseline `892a5ed` with 12 frozen scenario/wording holdouts through the production HTTP handler using an isolated history database. Sol-enabled mode produced 3 supported direct answers, 6 safe partial/missing-evidence responses, 2 model responses containing material errors, and 1 wrong deterministic lookup that bypassed Sol. The evaluator saw community replies during collection, so this is an unblinded assistant-graded source audit, not a general accuracy benchmark. Eleven Sol API calls used 9,369 input and 1,931 output tokens. All completed. All 39 existing automated tests still pass.

Highest-priority defects: a Waist injury question resolves the Head table; hunt-event damage is given showdown severe-injury consequences; reviewed records omit decisive rules from their cited pages, including attacker knockdown and Encourage timing. Next work is body-location/milestone validation, phase-aware source coverage, complete rule units, and regression checks followed by a new holdout. No application code or source records were changed, and this evaluation has not been committed or pushed. Details and artifacts are in `evaluation/2026-09-29/REPORT.md`. The prior verification paragraph's GitHub commit predates the canonical-location documentation commit; the tested baseline is `892a5ed`.

## Injury table guard, 29 September 2026

Fixed the first holdout defect in `kdm-assistant/engine.py`. Injury location checks now handle different word orders and singular/plural Arm and Leg wording, and apply even when a Head record is selected or retained in conversation context. Unreviewed locations return an unsupported response instead of a Head-table result. Multiple named locations require clarification; a Head-table roll without an established location also requires clarification. Explicit Head questions and numeric Head follow-ups still resolve.

Added five regression test methods in `test_core_rules.py` and `test_server.py`. The original H12 question and nearby variations reproduced the failure before the fix. All 44 automated tests pass after the fix, including HTTP checks in both local and Sol-enabled modes and saved-history checks. These checks use a mocked model service and made no API calls. No new source coverage was added. Changes remain local and uncommitted; an existing app process needs a restart to load the updated Python code.

Next: review and add the hunt-event damage exception, complete the source records identified in the evaluation, and validate Age milestone selection. Then rerun the evaluation questions and collect new holdouts. The other severe-injury tables still require reviewed records. This status is ready for `/compact` or a new session.

## Hunt-event test, 30 September 2026

The evaluation and injury guard above were committed and pushed to GitHub main as `a6d1a98` on 29 September. This supersedes their earlier uncommitted status notes.

Tested the proposed hunt-event body-damage question against that commit through the production HTTP handler with isolated chat history. Both local and Sol-enabled modes returned the missing Head-table coverage notice. The new guard mistakes a question about whether damage causes a severe injury for a request to resolve an injury table. Zero API calls were made. Source review of revised PDF pages 41, 47, and 48 confirms that ordinary hunt-event damage cannot cause severe injuries or brain trauma, while explicitly instructed event injuries remain an exception. Body damage does not reduce insanity. The question omits existing injury-box states, so the expected answer must state its assumption; an already-injured variant is needed to test damage overflow.

Saved the response and source audit under `evaluation/2026-09-30-hunt/`. Application code and rule records are unchanged. Next: narrow the table guard, add the complete hunt-event damage rule unit, and verify normal hunt damage, filled-box overflow, brain damage, explicit event instructions, and showdown contrasts. Then run a bounded live model retest. Today's evaluation and documentation changes remain local and uncommitted. This state is ready for `/compact` or a new session.

## Hunt-event fix and retest, 30 September 2026

Completed the fix described above. General damage questions now pass the injury-table guard, while actual unreviewed table results remain unsupported. Added a reviewed hunt-event record covering the complete Event Damage and Severe Injuries and Brain Trauma rule unit on revised PDF page 41, including its token-duration continuation, with supporting rules on revised pages 47 and 48. Current coverage is 16 topics on 22 source pages.

All 49 automated tests pass, including five new methods for hunt/showdown distinctions, filled boxes, brain damage, explicit event instructions, carryover, prior Head context, edition checks, evidence delivery, citations, and persisted responses. One live Sol retest returned the supported core ruling and explicit-event exception. Its brain-trauma answer remained implicit in the body-versus-brain distinction. The call used 563 input and 104 output tokens. Nearby variations have local and mocked integration coverage, not live model evaluation. See `evaluation/2026-09-30-hunt/REPORT.md` and `retest.json`.

Changes remain local and uncommitted. Next: complete the source units identified in the earlier evaluation, including attacker knockdown and Encourage timing, then validate Age milestone selection and rerun the broader evaluation before collecting fresh holdouts. This state is ready for `/compact` or a new session.

## Timing and Age tests, 30 September 2026

Completed seven targeted scenarios in local and Sol-enabled modes through the production HTTP handler, using isolated history and the uncommitted hunt fix above. Visually reviewed revised PDF pages 24, 50, 55, 56, and 81. All 49 existing automated tests pass. Three live Sol requests used 2,115 input and 460 output tokens, totaling 2,575 tokens. This is an unblinded assistant-graded source audit, not a general accuracy benchmark.

Confirmed missing attacker-knockdown cancellation evidence and incorrect Sol answers requiring a survival opportunity for Encourage. The source permits Encourage at any time subject to applicable restrictions. A first-milestone Age roll of 8 selects the correct reward, though its answer omits weapon-type selection. The second-milestone question without a roll gets a safe missing-evidence response from Sol. Adding a roll of 8 instead resolves the first milestone in both modes and awards a fighting art, where the second milestone grants +1 permanent strength. An unspecified Age milestone also defaults to the first table. A follow-up to the second-milestone question switches to an unrelated severe-injury location clarification.

Artifacts and exact prompts are in `evaluation/2026-09-30-timing-age/`. No application code or reviewed records were changed in this batch; normal app history was untouched. All changes remain local and uncommitted, including the earlier hunt fix.

Next: add regression coverage, complete the attacker-knockdown and Encourage rule units, fix relevant retrieval, validate Age milestone identity before table resolution, and preserve it across follow-ups. Unsupported milestones should abstain and unspecified milestones should ask. Then rerun the targeted batch before broader holdouts. This state is ready for `/compact` or a new session.

## Combat source tests, 30 September 2026

Completed six further scenarios in local and Sol-enabled modes: repeated monster movement, Claw versus Basic Action targeting, the wound threshold and Failure reaction, luck-based critical wounds below toughness, locations without critical effects, and Impervious. Used fresh chats and an isolated history database with the current uncommitted hunt fix. Questions and expected rulings were frozen before responses. Reviewed complete revised PDF pages 9, 45, 46, 51, 53, and 135.

Sol returned partial or missing-evidence responses in all six cases. No complete direct ruling or definite wrong ruling was identified in this batch. Local lookup returned related reference text without the decisive rules. Captured source payloads confirm missing monster-movement and Basic Action rules, threat definitions, the wound formula and threshold, and general critical-wound exceptions. C02's wording confuses a survivor facing the lion with the lion's facing area; its intended first-condition expectation is conditional, so correct that wording before a future pass/fail retest. The Claw record has the same wording risk.

Six live calls used 2,911 input and 990 output tokens, totaling 3,901 tokens. All 49 existing automated tests pass. This is an unblinded assistant-graded source audit of known coverage risks, not a general accuracy benchmark. Full artifacts are in `evaluation/2026-09-30-combat/`.

No app code, source records, or model prompt changed; no commit or push occurred. Earlier hunt changes and the September 30 evaluations remain local and uncommitted. Next: address the confirmed timing and Age errors, then complete these core combat rule units, add regression coverage, and run bounded live retests. This state is ready for `/compact` or a new session.

## Timing, Age, and combat fixes, 30 September 2026

Implemented the requested fixes in `engine.py`, `core_records.py`, and `records.py`. Attacker knockdown cancels unresolved hits; Encourage does not restore them. The survival record states Encourage's own timing, deaf-recipient restriction, action costs, unlock requirements, and shared restrictions, while retaining the separate monster-turn limitation. Attack evidence now includes the wound formula and threshold. Critical-wound evidence includes luck, no-critical-effect locations, Impervious, reaction cancellation, and persistent injuries. Added monster movement and target definitions, linked the pictured White Lion Basic Action and Sniff, and corrected the Claw facing wording. Coverage is 17 topics on 23 source pages.

Age resolution validates milestone identity before selecting a roll band. Unspecified, conflicting, and unrecognized milestones require clarification. Milestones 2-4 remain outside reviewed table coverage and return unsupported instead of first-milestone rewards. Short follow-ups preserve the milestone, while explicit topic changes can select other records. First-milestone outcomes include weapon-type selection and the lifetime limit. A roll given before a milestone clarification must be entered again after the milestone is identified.

Added 11 regression methods in `test_combat_fixes.py` and two HTTP methods in `test_server.py`, with updated coverage assertions. The new tests reproduced the defects before implementation. All 62 automated tests pass after the fixes, including saved Age context, model bypass for guarded table questions, source delivery, and citations. `git diff --check` passes. The README is updated. Restarted the production app hidden on port 8765; health reports 17 records, 138 pages, and Sol configured. History was preserved. The model prompt is unchanged.

Prepared `evaluation/2026-09-30-fixes/run.py` to rerun the 13 previous timing/Age and combat cases in both modes, with C02 facing wording corrected and an eight-call API cap. The live retest has not run yet. Awaiting the user's confirmation to reuse the saved questions and inspect targeted fields from the result files under their large-file reading rule. No API credits were used for this fix turn so far. No commit or push. Next: run and grade that retest after approval, address any remaining failures, then consider fresh holdouts. This state is ready for `/compact` if pausing here.

## Fix retest completed, 30 September 2026

After the user's approval, ran the prepared 13-case retest in local and Sol-enabled modes. All core ruling and safety expectations were met. The eight live answers now resolve the knockdown, Encourage, movement, targeting, wound-threshold, and critical-wound contrasts. Five Age cases bypassed the model: one first-milestone resolution, three second-milestone missing-coverage responses, and one milestone clarification. T07 retained second-milestone scope across its roll follow-up. Local mode supplies corrected reference text for general questions and the same guarded Age outcomes. C02's facing wording was corrected before requests and its original wording was retained in the artifact.

Eight live calls completed without retries, using 7,375 input and 880 output tokens, totaling 8,255. All 26 evaluation requests succeeded. All 62 automated tests pass; app health reports 17 records, 138 pages, and Sol configured. Normal chat history was untouched. No app code or model prompt changed during the retest. This is an assistant-graded regression check informed by the earlier findings, not an independent accuracy benchmark. See `evaluation/2026-09-30-fixes/REPORT.md` and its captured questions, responses, and metadata.

Remaining presentation issue: T01 generated unlabeled original-PDF page references in its prose. The response's clickable citations retain correct revised/printed/original mappings. This did not affect the ruling, but generated references should be made consistent with the app's numbering. Later Age milestones remain unreviewed. Next: address prose citation consistency, then collect fresh wording and counterexamples. All current fixes and September 30 evaluations remain local and uncommitted; nothing was pushed. This state is ready for `/compact`.

## Citation fix, 30 September 2026

Removed `original_pdf_page` from the model-only source payload in `sol_answer.py`. Added a separate Responses API `instructions` message that directs the model to omit page numbers, links, and citation markers, leaving navigation to the app's mapped clickable citations. Rule text and source records remain intact, including any embedded page mentions; the instruction covers those mentions too. The local citation metadata, deterministic responses, and saved historical answers are unchanged. Used official OpenAI documentation to select the higher-priority instructions field: https://developers.openai.com/api/docs/guides/text.

Two tests in `test_sol_answer.py` reproduced the missing contract before the fix and now pass. All 64 automated tests pass, including existing HTTP citation and persistence checks. One live retest of T01 returned the correct cancellation ruling with no page references, using 1,637 input and 54 output tokens, totaling 1,691. Exact output and the one-call harness are in `evaluation/2026-09-30-citations/`. This is one sampled response, not a guarantee that the model will always follow the format instruction. No model change or broader rules changes were made.

README updated. Restarted the app hidden on port 8765 and confirmed healthy status with 17 records and Sol configured. `git diff --check` passes. No commit or push. Next: fresh holdouts and continued coverage expansion; watch for citation-format regressions. This state is ready for `/compact`.

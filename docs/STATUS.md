# Current project status

Updated 24 October 2026 for the user-authorized consolidation onto `main`, following the early-campaign coverage and diagram/source-context repair. This is the single current handoff. [History](history/README.md) preserves previous snapshots and superseded instructions.

## Objective and phase

The objective is a source-grounded assistant for the group's 1.5 play. The first release focuses on the Prologue, first settlement, first level 1 White Lion hunt/showdown, and its returning settlement. The [release checklist](RELEASE_CHECKLIST.md) defines requirements R01–R14, exclusions, source gaps, and gates. [The roadmap](OBJECTIVE_AND_ROADMAP.md) owns phases. Baseline routing/table/follow-up failures have targeted repairs and passing regression checks; required coverage and broader release evaluation remain open.

## Application state

- Rules/source development: `D:\Documents\KDM\KDM-Rulemaster-v2`, branch `rules-v2`, checkpoint `1670bc1`. The user-authorized integration combines it with `main` at `D:\Documents\KDM\KDM-Rulemaster`, preserving the existing access-gate commits. The combined tree passes 128 tests, including both shared-access tests. [Integration notes](MAIN_INTEGRATION.md) record scope and preservation checks.
- 33 reviewed topics across 36 source pages; all 138 retained rulebook page images are available. [Coverage](COVERAGE.md) lists the reviewed topics.
- Local lookup is default. Optional GPT-6 Sol explanations use selected reviewed records. Supported exact tables resolve in code. Coverage remains limited.
- Latest additions: eight bounded units for Basic Action/reference faces, killing wound, separate Prologue and level 1 aftermath, first-settlement return/development/crafting/storage, hunt progression, and level 1 attributes/deck construction. Ground Fighting's linked diagram and untranscribed geometry limit now reach the model.
- Six physical White Lion photos back Claw, Grasp, Maul, Combo Claw, Power Swat, and Size Up work. Wiki drafts remain unreviewed and outside runtime retrieval.
- Cunning remains an unverified gap and is excluded from active work.
- Automatic deployments are disabled in repository configuration for `main` and `rules-v2`. The requested GitHub consolidation is separate from a production release. Coverage, device, and protected-hosting gates remain open. [Integration notes](MAIN_INTEGRATION.md) record the promotion and validation.

## Release preparation completed

The [early-campaign source audit](../evaluation/2026-10-24-early-campaign-coverage/REPORT.md) records the new evidence and development checks. All 126 Python tests pass. The final HTTP snapshot saves 33 responses: 17 new local cases, seven live Sol versions, and nine affected baseline turns. All 24 new source selections and nine affected source/boundary decisions matched expectations. All seven live answers were reviewed; both diagram cases identified the available image and left exact untranscribed squares unresolved. These checks do not establish release readiness.

Supporting sources now prioritize declared dependencies and preserve encounter/phase scope. Standard deployment brings in random 7 Basic/3 Advanced deck construction. Generic killing-wound rules are separate from Prologue rewards. Sol receives layout and image-availability metadata with interpretation limits, without image pixels. First Day/Language card effects, full eligible deck inventories, and complete repeating settlement rules remain missing.

The first coverage run and final repair run are preserved separately: 13 successful Sol calls, 13,207 tokens total, no API fallbacks or automatic paid retries. Both checked 20 local citation images over HTTP. The original 81 baseline files retain the same aggregate fingerprint. Key access stayed in memory; `main` remains unchanged. No commit, push, or deployment was made.

Latest repair: primary references require topic evidence; named missing sources cannot borrow adjacent rules; completed card mentions no longer replace the requested source; Prologue and standard setup remain separate. Age/table identity and natural final/total-roll phrasing are parsed before exact resolution. Unsupported injury context preserves the topic/location for a correction, while explicit new topics can leave it. Branding uses the supplied roll without requesting another. No new rule records or model-prompt changes were made.

The preceding retrieval repair passed 115 Python tests, including local/hosted context integration. Its [regression report](../evaluation/2026-10-24-retrieval-regression/REPORT.md) preserves a final HTTP run of 16 affected scenarios and 20 turns per mode: all 40 targeted source/table decisions passed. Three final responses used Sol; the other Sol-requested turns used deterministic reference-boundary/table handling. This was not complete answer or release acceptance. Local no-target prose remains limited; the current coverage batch adds standard deck-construction evidence.

That preceding repair also byte-preserved the original 81 baseline files. Its six successful Sol calls used 3,752 tokens total. The Ground Fighting diagram-availability issue remained open at that checkpoint and is addressed by the current batch.

Created the first-release checklist with open requirements for starting setup/gear, combat, eligible Prologue/level 1 AI and hit-location decks, injury/brain rules, survival/unlocks, aftermath/first Age, initial settlement, crafting procedure, hunt sequence, Tall Grass, and context transfer. Complete random event/gear/innovation libraries and later campaign content are excluded. Full eligible deck inventories and missing fixed early rules remain required evidence work. Cunning has no active evaluation case.

The [baseline results](../evaluation/2026-10-24-release-baseline/REPORT.md) cover all 32 scenarios and 36 turns per mode, including four two-turn conversations. There were 30 actual Sol calls, six deterministic responses in Sol mode, and no request failures, fallbacks, or retries. All 72 first responses and separate grades are preserved. Questions remain version 1 and key answering inputs matched before/after. No runtime records, retrieval, model prompts, or automated tests were changed for this evaluation.

Local response review: 14 pass, 9 partial, 13 fail. Sol-requested response review: 29 pass, 2 partial, 5 fail. These include correctly acknowledged required gaps and are not full-source or readiness passes. Reviewed-topic turns alone were local 10/7/3 and Sol-requested 15/2/3. The report separates covered-topic errors, required evidence gaps, exclusions, and execution outcomes.

The preserved first pass exposed Chomp/Claw substitution, wrong encounter selection, Age attracting aftermath/event questions, missing natural roll wording, and a lost Head correction. These now have regression repairs described above. The original Sol error about Head injury boxes is avoided by resolving the supported table before model composition. This does not establish unrestricted injury reasoning. The current batch addresses the separate diagram-availability finding.

The user authorized reading `D:\Documents\KDM\KDM-Rulemaster\.env` in memory for the run. No key was copied into this checkout or printed, and no file in `main` was modified. Successful calls used 24,745 input and 3,945 output tokens (28,690 total). The temporary process/server/history are closed.

The set is source-guided and authored after exposure to prior work; it is not an independent blind benchmark. Once used for repairs, these cases become regression fixtures. A new unseen batch is required for final release evaluation.

## Cleanup completed

Added root navigation and separate current roadmap, status, sources, coverage, and evaluation navigation. Archived old status/iteration documents, the previous app guide, OCR planning, and design previews. Grouped the player handout under player material and community scenarios under evaluation. PDFs and their map are in `sources/`; asset preparation references were updated.

The app, active tests, served images, local original evidence, and existing dated evaluation folders keep their established paths. Dormant wiki tools and tests remain in place to preserve imports and saved commands; detailed instructions are archived. No useful source or historical result was deleted. The empty `tmp/` folder was left in place after automatic approval review blocked the initial combined housekeeping command; file moves succeeded without deletion.

## Verification and limits

The preceding card batch passed 100 Python tests. Its twelve source-guided development cases matched expected source/boundary categories after changes. Those are regression results, not an independent accuracy estimate. No live Sol evaluation was run for that batch.

All 101 Python tests pass after cleanup, including an isolated asset-rebuild check for the relocated page map and focused-PDF path. The coverage generator checked all local evidence links before writing. Moved files preserved their lengths, navigation targets exist, and `git diff --check` passes. See the [cleanup record](../evaluation/2026-10-24-folder-cleanup/REPORT.md) for preservation details and checks. No new live Sol or deployment evaluation was performed.

## Next actions

1. Acquire missing Chomp/Terrifying Roar/full Enraged faces and establish the eligible 1.5 AI/hit-location inventories. Preserve the bounded rulebook evidence added here; do not promote dormant drafts without review.
2. Review First Day, Language, full Returning Survivors, initial location faces/recipes, repeating settlement rules, Tall Grass, and remaining injury/Brain Trauma units. Cunning stays excluded. Historical queues remain paused.
3. Run new unseen source-selection, multi-card/context, and explanation scenarios after the coverage/process work. Saved baseline cases remain development/regression fixtures; their passes do not establish independent accuracy.
4. Before group use, address launcher identity: it can open a different checkout already running as the same app on port 8765. The audit inferred this risk from code; it has not been reproduced.

Historical OCR/wiki queue entries are not active tasks. This state is ready for `/compact` or a new session.

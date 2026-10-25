# Reviewer guide and run protocol

This file is for the evaluator. Do not send it, the checklist, expected sources, or answer hints to the answering app. [Questions](QUESTIONS.md) are version 1, fixed before their first run. [The checklist](../../docs/RELEASE_CHECKLIST.md) defines required versus excluded coverage. No baseline has been executed.

## What this batch establishes

This is a source-guided initial release baseline, authored after exposure to records and prior evaluations. It includes new scenarios and phrasing, several topics already used in regression work, and planned coverage gaps. It is not an independent blind accuracy estimate. Cases used to fix the app become regression cases. Final release requires another unseen batch after those fixes.

There are 32 scenarios, 36 user turns per mode, and two requested modes. A full paired run has 72 response records. Sol requests do not guarantee a model call: deterministic results, declines, disabled/unavailable configuration, and other boundaries may stay local. Record whether the model was actually used. Do not mark an unexecuted or fallback model path as tested.

## Run procedure

1. Record the commit and dirty-worktree state, question version, app version/checkout, start time, and selected mode. Use this `rules-v2` checkout, isolated history, and a nonconflicting port. Leave `main` untouched. Do not deploy.
2. Run the local-only mode first without changing code, records, prompts, or sources. Start a new chat for each scenario. Feed the actual returned context into the next turn of Q19, Q20, Q30, and Q31; do not provide a corrected record ID or reviewer hint.
3. Run the optional Sol mode with the same prompts in separate fresh chats. Use only the app's normal selection and explanation path. Stop and report configuration failure instead of borrowing credentials from another checkout or treating fallback text as a Sol answer. Configure through the documented local paths or environment when authorized.
4. Preserve the first response to each prompt, selected primary/supporting records, source links, response category, actual model use, and execution errors. A missing response is an execution failure, not a decline. Record paid-call counts and usage when available. Do not perform automatic paid retries or tune between modes.
5. Review outputs against actual source images and scoped text. Do not treat a lexical match or expected record ID as proof of correctness. A different source set may pass if it supplies all applicable evidence. Preserve disagreements and uncertainty.
6. Read/report targeted outputs in batches consistent with the user's data-reading limits. Keep raw records separate from the report. Summarize failures by cause before proposing fixes.

Only question/run artifacts are being created now. No API call, source acquisition, app change, or test execution is part of preparing this batch.

## Grading dimensions

For every turn record `pass`, `partial`, `fail`, or `not run` for:

- **Evidence:** applicable card/rule units and necessary linked definitions were selected; no substitute from an unrelated card, phase, table, or edition.
- **Meaning:** material conditions, order, arithmetic, and exceptions are correct. Distinguish exact outcomes from examples and assumptions.
- **Response:** actionable for covered questions, useful clarification when context is missing, and explicit limits when evidence is absent. Local reference mode can present a correct bounded reference; it need not mimic Sol's prose.
- **Sources:** citations open the correct image/page, with consistent identifiers and supported provenance claims.
- **Context:** multi-turn cases retain the right facts and replace changed facts. Mark this dimension not applicable for single-turn cases.

A material error changes a legal action, target, result, cost, timing, reward, or compatibility claim. Record critical unsupported invention even when other dimensions pass. Do not average it away in a score.

## Expected source and behavior targets

These are reviewer targets, not a complete mechanical answer key. Recheck the cited images before final grading. For sources not yet reviewed, do not invent the missing card or event text in this guide.

| Cases | Evidence and behavior to check | Baseline versus release |
| --- | --- | --- |
| Q01–Q02 | Create a Survivor and First Story setup. Naming grants survival; only Dodge starts available. Preserve Claw/Strange Hand top-card preparation and shuffling of the remainder. | Reviewed evidence exists; evaluate usable explanation and distinctions. |
| Q03–Q04 | Survivor act/attack rules and Founding Stone face. Completed activation and movement have their own order; normal attack and sling have different instructions. Use the printed profile and strength rules, without applying a sling critical to a normal attack. | Relevant records exist; inspect source completeness. |
| Q05–Q06 | Victory, empty AI deck/discard, aftermath, rewards, gear/resource disposition, and XP need their full rule units. Emptying the AI supply and killing the monster are distinct steps; check the actual tutorial/aftermath source before grading. | Required R03/R09 gaps. A scoped source-needed answer is honest today, while release remains blocked. |
| Q07 | Claw plus target definitions/controller tie choice. Preserve the first eligible target condition and who resolves a tie. | Reviewed evidence exists. |
| Q08–Q09 | Power Swat/Size Up faces plus After Damage, Dodge, insanity, and knockdown rules. A fully dodged Swat does not trigger After Damage; Size Up is Intimidate, and insanity protects against its brain damage while knockdown remains a printed effect. | Reviewed evidence exists; evaluate arithmetic and trigger separation. |
| Q10–Q11 | Maul face, Grab definition, and attack-profile/token rules. The first Maul target condition does not require the prior victim to remain knocked down. Selection does not perform Grab. The bounded level 1 damage-token example may support Maul's profile, without certifying full Enraged. | Reviewed evidence exists; ensure evidence is combined and the scope stays bounded. |
| Q12 | Combo Claw photo, Strange Hand, and persistent-injury rules. Lost Hand replaces normal AI actions; apply the once-per-lifetime limit to each survivor, with no normal attack/conditional draw. | Reviewed evidence exists. |
| Q13 | Ground Fighting face and Zone of Death, with activation/movement distinction. Test the actual trigger rather than treating presence or movement through a zone as an activation. | Reviewed evidence exists; the diagram must be accessible. |
| Q14–Q15 | Strange Hand optional survival reward/persistence; Clever Ploy, general Trap/Doomed rules, and simultaneous-attack handling. Do not invent a free strength reward, retain remaining attacks after a Trap, or extend restrictions beyond the source. | Reviewed evidence exists; check complete applicable source units. |
| Q16–Q18 | Each named AI face and linked rules, including complete mood entry/ongoing/discard text. The tutorial damage example alone cannot establish the full Enraged card. | Required R05 gaps. Source-needed is an acceptable baseline boundary; complete verified card coverage is required to close release. |
| Q19 | Turn 1 needs the card identity or a conditional explanation. Turn 2 must use Power Swat's no-target instruction and applicable Sniff definition. Do not carry forward an unspecified generic attack. | Clarification followed by covered evidence. |
| Q20 | Separate First Story setup from standard level 1 deployment/deck rules when the user changes the encounter. The existing deployment record does not certify complete deck/level setup. | Partial R02 evidence. Credit a sourced partial answer with explicit missing pieces; do not count partial as release completion. |
| Q21–Q24 | First-settlement sequence, First Day, Language/action unlocks, locations, storage, and crafting procedure need reviewed complete sources. Q24 must request exact recipe/card information for exact costs. | Required R08/R10/R11 source gaps. General nearby survival or affinity records are insufficient substitutes. |
| Q25 | Exact hunt-event 84 requires its reviewed table entry. Without it, state missing coverage and request the event text/source. Do not supply a plausible event from memory. | Specific event catalog is excluded. A correct boundary can pass release. |
| Q26 | Tall Grass tile count has deployment support; hiding requires the actual terrain effect and relevant rules. Distinguish that partial evidence from a fully reviewed terrain face. | Required Tall Grass effect evidence gap under R13. |
| Q27 | Hunt setup/movement/event/arrival procedure needs the relevant reviewed rulebook unit. A hunt-damage record alone is insufficient. | Required R12 source gap. |
| Q28 | Hunt damage exception and persistence: existing injury boxes cannot absorb more damage, ordinary hunt damage does not cause a severe-injury roll, and existing marks persist into the showdown. Do not apply normal showdown overflow or invent a severe result. | Reviewed evidence exists. |
| Q29 | First Age milestone and its actual table: choose weapon type, apply the 13 band, and distinguish proficiency eligibility from an immediate proficiency level. No later milestone substitution. | Reviewed evidence exists; exact outcome should remain deterministic where supported. |
| Q30 | Use the reviewed Hands of Heat branches and exact 6 bands. Treat the second turn as a separate occurrence with Lantern Oven already present. Do not keep an earlier branch solely from context. | Existing reviewed optional event; tests state/table transfer. |
| Q31 | Turn 1 requires the Arms table, not Head. Turn 2 changes the location to Head; reviewed Head 8 is Concussion with its listed effects. | Arms is a required R07 gap today; Head evidence exists. Score honesty and successful context replacement separately. |
| Q32 | State that 1.5 evidence does not verify 1.6. A version change requires checked edition-specific sources; no automatic certification. | Explicit out-of-scope edition boundary. |

## Report requirements

Keep these findings separate: (1) covered-topic errors, (2) missing required evidence, (3) correct excluded-topic boundaries, and (4) execution/model-use failures. Count scenarios and turns by mode, and name every not-run item. Show first-pass results before any development reruns. Do not combine missing required coverage with successful declines into a single readiness percentage.

A release blocker is any open required coverage row, material answer error within scope, fabricated missing result, wrong source citation, or failure to preserve a material scope/context boundary. The initial batch diagnoses work; final acceptance uses the gates in the checklist and a newly authored batch after fixes.

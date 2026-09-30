# KDM holdout evaluation

29 September 2026. Baseline: `892a5ed1031f29b1e59f15ed42c178304e1ec69f`.

## Conclusion

The app needs stronger source coverage and question-to-record validation before it can be trusted for general rules answers. Sol recognized several missing sources, but also produced an incorrect hunt-damage ruling and an unsupported Encourage restriction. A deterministic lookup returned a Head injury for a Waist question. A more expensive model would not repair that local routing error.

No application code, prompts, or reviewed records were changed during this evaluation. Nothing was committed or pushed.

## Method and limits

- Froze 12 new question wordings in `questions.jsonl` before testing. Ten adapt community questions or thread follow-ups; two are evaluator-authored coverage boundaries. Their subjects overlap existing coverage, so this is a wording/scenario holdout, not a wholly new-topic benchmark.
- Community search results exposed replies to the evaluator. This is an unblinded, assistant-graded evaluation. Community replies were not sent to the app and were not used as authoritative rulings.
- Used the unchanged production HTTP handler with a temporary history database and a fresh conversation for each request. Each question was submitted once with local lookup and once with Sol enabled. The live app's history was untouched. Browser interactions and multi-turn behavior were outside scope.
- Sol used its existing low-effort setting, three-record source limit, and 700-token output limit. It received the question and existing source records, with no evaluator answers or additional rulebook text.
- Reviewed the relevant existing page images against the edition 1.5 scan. Page references below use revised PDF numbering first. A page being cited does not mean all its rules have been captured in the app's record.
- Graded direct answers, safe recognition of missing evidence, and materially misleading answers separately. Local lookup was assessed as a reference-returning feature rather than expected to synthesize free-form rulings.
- This single run does not establish general accuracy, model consistency, or expert-human agreement. H08's underlying armor exception remains unverified; its abstention was assessed against the supplied records.
- The OpenAI Docs skill informed the separation of outcomes and limitations, following [official evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices). The PDF skill drove visual verification of the rules and their page mappings.

Question-file SHA-256: `84b8b3c89cdd5d86f60442a0cfedd6c32eb503c05dcda54c3f8c1a461c7dfa7e`.

## Results

With Sol enabled across all 12 requests:

- 3 supported direct answers: H05, H06, H10.
- 6 safe missing-evidence or partial-answer responses: H02, H03, H04, H08, H09, H11. These are safety successes but leave some or all of the player's question unanswered.
- 2 model responses containing material errors: H01, H07.
- 1 wrong deterministic result that bypassed Sol: H12.

Local mode returned 11 generic references and 1 resolved table result. It never returned an unsupported status for this set. Several references were relevant but incomplete. H11 disclosed its narrower scope in a note; H12 resolved the wrong body-location table. The model-enabled results therefore should not be described as 12 independent model answers.

| ID | Scenario | Local lookup | Sol-enabled result |
|---|---|---|---|
| H01 | Encourage after an attacker's knockdown | Attack sequence omits the cancellation rule | Flags missing rule, then adds incorrect restriction on Encourage timing |
| H02 | White Lion moves again for a reaction | Survivor movement/attack reference misses monster movement | Safe abstention |
| H03 | Knocked-down survivor versus threat | Claw instructions omit the requested distinction | Safe abstention |
| H04 | Hit versus wound and Failure reaction | Relevant sequence, missing wound formula | Correct partial answer; admits formula is absent |
| H05 | Three damage to one random location | Relevant per-hit damage reference and related effects | Correct: one location roll, all three damage there |
| H06 | Knockdown from first of two hits | Relevant sequential-hit rules | Correct: body hit still resolves under stated assumptions |
| H07 | Hunt-event damage and severe injuries | Supplies showdown damage rules without hunt exception | Incorrect: says ordinary hunt-event damage causes severe injuries |
| H08 | Armor and checked injury boxes coexist | Damage-order reference cannot settle armor restoration | Safe abstention; actual exception not independently verified |
| H09 | Natural 9, +1 luck, below toughness | Retrieves critical examples without governing rule | Safe abstention |
| H10 | Second Dodge in the same round | Primary damage reference omits limit; related record contains it | Correct: changing turns does not reset once-per-round limit |
| H11 | Age at 6 Hunt XP | Returns first milestone; note excludes later milestones | Safe abstention and warns against reusing first table |
| H12 | Waist severe injury, result 8 | Wrongly resolves Head 8 | Same wrong local answer; no model call |

Exact prompts, provenance URLs, raw responses, selected records, citations, and timing are retained in the adjacent question and result files.

## Source audit and causes

### H01: omitted rule plus a timing overreach

Revised PDF 50, printed 73, original 77 says a survivor knocked down during their own attack has their unresolved hits canceled. Standing afterward does not restore them. This decisive rule is on a page already cited by the attack-sequence record, but the record omits it.

Revised 55, printed 78, original 82 says a standing survivor may Encourage at any time, subject to the other applicable restrictions. Sol instead stated that Encourage requires an allowed opportunity and cannot be used at any moment. The supplied survival record omits the explicit Encourage timing sentence and describes broader survival windows, which invites this mistaken generalization. This response cannot count as a safe abstention despite admitting the missing knockdown rule.

### H02 and H03: pages contain more than the records

Revised 46, printed 69, original 73 defines Move & Attack Target for each instructed action. Revised 9, printed 27, original 31 shows the White Lion Basic Action with Move & Attack Target. Revised 135's Movement glossary defines the movement allowance per single action. The lion may move again when instructed by the reaction's Basic Action. The selected survivor-attack record lacks this evidence.

Revised 45, printed 68, original 72 defines a threat as a survivor who is not knocked down or otherwise hidden from threat status. Revised 9 contrasts the Basic Action's survivor targeting with Claw's threat targeting and includes Sniff's override. Knockdown does not exclude a survivor from all targeting. Sol's abstention reflects an incomplete Claw record; its cited page contains the missing distinction.

### H04: wound formula lost from a reviewed page

Revised 51, printed 74, original 78 gives the wound attempt: roll 1d10, add weapon strength and survivor strength modifiers, and compare with toughness including modifiers. Failure reactions follow failed wound attempts. A hit does not deal Strength as automatic damage. The record preserves the step order but omits the formula, so Sol declines to provide it even though the cited page supplies it.

### H05 and H06: successful applications of damage rules

Revised 47, printed 70, original 74 gives per-hit locations, damage order, and separate resolution of hits. Revised 48, printed 71, original 75 says to roll a location when damage outside an attack profile specifies none. H05's single random-location instruction supports one location roll for all three damage. H06's remaining body hit persists after knockdown, under its explicit survival/attack-continuation assumptions. Revised 10, printed 28, original 32 also instructs players to apply all hits.

H05's model prose cites “p. 75” and “p. 74.” Those are original-scan identifiers supplied to the model. They are not revised or printed page numbers. The page references are traceable, but their unlabeled format conflicts with the project's revised-page default. The structured citation mappings are correct.

### H07: phase exception missing

Revised 41, printed 63, original 67 states that ordinary hunt-event damage can reduce armor/insanity and mark light/heavy injuries, but does not cause severe injuries or brain trauma. Explicit event instructions can cause those separately. Revised 133's Event Damage glossary confirms that exception.

Sol applied the showdown section about damage outside attack profiles to hunt-event damage and asserted severe injuries occur. That contradicts the hunt rule. The supplied records lack phase scoping and the event-damage exception. The inspected event-damage passage does not itself settle every knockdown-timing detail, so the failure judgment rests on the clear severe-injury contradiction rather than an assumed knockdown ruling.

### H08: abstention is appropriate for the supplied evidence

Revised 47 establishes armor-first damage order. It does not establish all armor-restoration, direct-injury, or injury-clearing exceptions. Sol identifies the missing evidence instead of claiming coexistence is impossible. A concrete edition 1.5 example still needs source verification before adding a definitive tracker-design answer.

### H09: examples need their governing rule

Revised 53, printed 76, original 80 says +1 luck extends the critical range to natural 9, a critical wound wounds below toughness unless Impervious, and a location with no critical effect cannot be critically wounded. Luck does not turn a 9 into a natural lantern 10. Thus the stated 9 wounds a critical-capable, non-Impervious location; without a critical effect, the below-toughness result fails. Other explicit card restrictions still apply.

The app retrieves only revised 54's worked examples. Sol recognizes their missing premise and abstains. This is a source-unit completeness problem.

### H10 and H11: useful limits

Revised 55 limits each survival action to once per round. Revised 56 ends the round after the survivors' turn. Sol uses the related survival record to answer H10 correctly despite the primary record being damage order.

Revised 24, printed 43, original 47 shows the Hunt XP milestones. Revised 81, printed 107, original 111 provides separate Age tables. Six XP uses the second milestone, Improved Reflexes, with a 2d10 table: 2 movement +1; 3-6 one random fighting art; 7-15 strength +1; 16-19 one random fighting art; 20 speed +1. Attribute gains are permanent. The current record explicitly covers only the first milestone. Sol correctly refuses to substitute it.

### H12: wrong body-location lookup

Revised 63, printed 87, original 91 gives Waist 8: Slashed Back, cannot Surge until the showdown ends, and gain one bleeding token. The app instead returns Head 8: Concussion, a random disorder and one bleeding token, citing revised 62, printed 86, original 90.

The missing-table guard expects the body location directly after “severe.” The test's phrase “severe injuries table for my waist” misses that pattern. Search then selects the Head record, parses 8, and resolves it without checking that the requested body location matches. Sol is bypassed because the local result is already marked resolved. Both pages exist and their mapping is correct; the selected table is wrong.

## Prioritized next work

1. Validate body location and milestone identity before deterministic resolution. Unknown or uncovered details should produce a clear missing-source response, regardless of word order.
2. Add the hunt-event damage exception and explicit phase scope. Avoid presenting showdown damage as a universal rule.
3. Complete the existing source units: attacker knockdown, Encourage timing, wound formula, critical-wound rules, and survivor/threat targeting. These gaps exist on pages already available to the app.
4. Separate full answers, partial references, and missing evidence in the response state. Have the model use application-provided citations with explicit revised/printed/original labels.
5. Turn these failures into regression cases, then collect another untouched question set. A rerun of these questions after fixes measures regression progress rather than fresh holdout performance.

## Execution record

The run made 11 API calls. All returned completed responses; no output-limit truncation or service fallback occurred. Reported usage was 9,369 input tokens and 1,931 output tokens, totaling 11,300. No dollar cost is claimed because billing was not inspected. No Astra API calls were made.

All 39 existing automated test methods passed after the evaluation. They did not detect the failures above. Question-file integrity, response metadata, and raw responses are retained in `questions.jsonl`, `run-metadata.json`, and `results.jsonl`. No secrets were included in those artifacts.

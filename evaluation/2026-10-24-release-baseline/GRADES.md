# Per-turn response review

Assistant-graded, source-guided first pass. These response grades are not full release passes: an acknowledged required source gap remains open, and evidence/citation relevance is graded separately in `grades.csv`. No overall accuracy or readiness percentage is reported.

`Pass` means the response meets the baseline behavior target, including a justified missing-source response. `Partial` means useful content with a material omission or ambiguity. `Fail` means an incorrect rule, wrong scope, irrelevant response, or unhelpful clarification. Local reference mode is allowed bounded reference text; it is not required to imitate model prose.

| Turn | Scope | Local response | Sol-requested response | Finding |
| --- | --- | --- | --- | --- |
| Q01.1 | covered | pass | pass | Starting survival and Prologue unlock restriction are supported. |
| Q02.1 | covered | pass | pass | Claw and Strange Hand top-card setup and remainder shuffling are supported. |
| Q03.1 | covered | pass | pass | Completed activation can precede movement within the act. |
| Q04.1 | covered | partial | pass | Local gives profile/sling text but omits the wound-roll formula; Sol combines related notes into 1d10 + 1. |
| Q05.1 | required gap | fail | pass | Local returns Clever Ploy instead of victory rules; Sol identifies the missing monster-death rule. |
| Q06.1 | required gap | fail | fail | Both modes ask an unrelated Age milestone question instead of addressing aftermath or its missing sources. |
| Q07.1 | covered | partial | pass | Local omits controller tie choice from rendered related text; Sol uses the supporting record notes. |
| Q08.1 | covered | pass | pass | After Damage requires damage; a dodged only hit does not cause the knockback. |
| Q09.1 | covered | partial | pass | Local states the effect but omits insanity arithmetic; Sol gives insanity 1 and knockdown. |
| Q10.1 | covered | pass | pass | Prior Grab victim remains first target condition and selecting them does not repeat Grab. |
| Q11.1 | covered | partial | pass | Local omits the supplied damage-token calculation; Sol gives Damage 4 and no repeated Grab. |
| Q12.1 | covered | pass | pass | Lost Hand replaces normal actions; lifetime understanding limit remains applicable. |
| Q13.1 | covered | pass | partial | Sol gives correct trigger but claims the diagram is missing despite the app card citation linking it. |
| Q14.1 | covered | pass | pass | No survival payment means no strength reward; Lost Hand still remains in play. |
| Q15.1 | covered | pass | pass | Trap stands the monster, ends both attacks, and restricts survival until resolved. |
| Q16.1 | required gap | fail | pass | Local returns Claw instructions for Chomp; Sol declines the missing Chomp card. |
| Q17.1 | required gap | fail | pass | Local repeats the setup list; Sol identifies missing Terrifying Roar instructions. |
| Q18.1 | required gap | pass | pass | Both acknowledge the full Enraged card is unreviewed; the existing example remains bounded. |
| Q19.1 | clarification | pass | pass | Asks which card determines the no-target instruction. |
| Q19.2 | covered | partial | pass | Local names Sniff but does not explain that it replaces the attack; Sol states no move-and-attack. |
| Q20.1 | covered | fail | fail | Prologue wording selects standard deployment; Sol falsely requests an available First Story record. |
| Q20.2 | required gap | partial | pass | Standard deployment is available but deck composition is outside the record; Sol states that limit. |
| Q21.1 | required gap | fail | pass | Local returns fight setup for settlement sequence; Sol requests the actual settlement sources. |
| Q22.1 | required gap | fail | pass | Local returns combat rules for population/First Day; Sol acknowledges the missing event. |
| Q23.1 | required gap | fail | pass | Local gives starting-survivor rules for Language; Sol identifies missing innovation evidence. |
| Q24.1 | required gap | fail | pass | Local gives starting gear rather than crafting; Sol identifies missing procedure and recipe sources. |
| Q25.1 | excluded event | fail | fail | Hunt event 84 is misrouted to Age clarification in both modes. |
| Q26.1 | required gap | partial | pass | Tile count is supported; Sol identifies missing Tall Grass effect instead of claiming complete coverage. |
| Q27.1 | required gap | fail | pass | Local returns showdown deployment for hunt procedure; Sol identifies the hunt-rule gap. |
| Q28.1 | covered | pass | pass | Ordinary hunt overflow causes no severe-injury roll and checked boxes persist. |
| Q29.1 | covered | fail | fail | First heavy-bordered Hunt XP wording is not recognized; both ask for a milestone already identified. |
| Q30.1 | covered | partial | pass | Local does not resolve final 6; Sol gives the correct experiment 4-6 band and no Branding roll. |
| Q30.2 | covered | partial | partial | Local still offers generic table selection; Sol selects Branding 4-7 but asks for a new roll despite the supplied current 6. |
| Q31.1 | required gap | pass | pass | Correctly declines the unreviewed Arms table without substituting Head. |
| Q31.2 | covered | fail | fail | Corrected Head follow-up selects hunt damage. Sol falsely says Head table is absent and mentions two Head injury boxes. |
| Q32.1 | edition boundary | pass | pass | Declines to certify 1.6 from the 1.5 collection. |

Five dimensions are recorded per mode/turn in `grades.csv`: evidence, meaning, response, sources, and context. Source-target existence/mapping checks are distinct from semantic relevance. An irrelevant attached source can fail evidence/sources while a model response correctly declines to invent the missing rule.

The two Q30 turns include table prose generated by Sol because the normal parser failed to select exact outcomes. The correct first outcome does not establish that the deterministic table path worked. The second answer adds an unnecessary new-roll instruction despite acknowledging the proper Branding branch and 6 band; it is graded partial rather than credited as full state handling.

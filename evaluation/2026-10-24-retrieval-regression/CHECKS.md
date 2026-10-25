# Affected source and table decisions

These are development/regression checks against the frozen baseline, not new holdouts or a release-readiness score. A correct unsupported decision means the app respects a gap; it does not add that missing rule. CSV fields preserve before/after source selection by mode.

| Turn | Expected final decision | Local | Sol-requested |
| --- | --- | --- | --- |
| Q05.1 | unsupported | pass | pass |
| Q06.1 | unsupported | pass | pass |
| Q16.1 | unsupported | pass | pass |
| Q17.1 | unsupported | pass | pass |
| Q18.1 | unsupported | pass | pass |
| Q19.1 | clarify | pass | pass |
| Q19.2 | reference: white-lion-power-swat | pass | pass |
| Q20.1 | reference: white-lion-setup | pass | pass |
| Q20.2 | reference: white-lion-deployment | pass | pass |
| Q21.1 | unsupported | pass | pass |
| Q22.1 | unsupported | pass | pass |
| Q23.1 | unsupported | pass | pass |
| Q24.1 | unsupported | pass | pass |
| Q25.1 | unsupported | pass | pass |
| Q27.1 | unsupported | pass | pass |
| Q29.1 | resolved: age-first-milestone / first | pass | pass |
| Q30.1 | resolved: hands-of-heat / experiment | pass | pass |
| Q30.2 | resolved: hands-of-heat / branding | pass | pass |
| Q31.1 | unsupported | pass | pass |
| Q31.2 | resolved: severe-head-injury / head | pass | pass |

The three model-generated answers in the final run were read in full: Q19.2, Q20.1, Q20.2. They select Sniff without the attack, explain the Prologue fixed setup, and keep standard deployment distinct while acknowledging the missing standard deck source. Exact Age, injury, and Hands of Heat outcomes now bypass model composition.

Local Q19.2 remains reference text naming Sniff rather than a composed no-attack explanation. Standard deck composition in Q20.2 remains missing required coverage. Passing this table verifies targeted source/table decisions, not complete answers to every release question. The earlier Ground Fighting image-awareness issue was not part of these changes.

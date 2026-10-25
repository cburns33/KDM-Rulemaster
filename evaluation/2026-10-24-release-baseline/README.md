# Opening White Lion and early-campaign baseline

First-pass run and review complete, 24 October 2026. Questions remain frozen as version 1. Both modes completed on the unchanged app snapshot. See [results and limitations](REPORT.md) and [per-turn grades](GRADES.md). No app changes or repairs were made during this run.

- [Questions](QUESTIONS.md): 32 scenarios and 36 user turns, including four two-turn conversations.
- [Reviewer guide](REVIEWER_GUIDE.md): actual-path run procedure, evidence/meaning/citation/context grading, and covered versus required-gap versus excluded-topic handling. Keep this file out of the answering app's input.
- [Release checklist](../../docs/RELEASE_CHECKLIST.md): requirements R01–R14, scope boundary, source gaps, and acceptance gates.

| Mode | Executed turns | Status |
| --- | --- | --- |
| Local-only | 36 of 36 | First responses preserved |
| Optional Sol | 36 of 36 | 30 model calls; 6 deterministic boundary/clarification responses |

Each scenario started a new conversation, with context retained within Q19, Q20, Q30, and Q31. First outputs, selected records, actual model use, input fingerprints, and token usage are preserved. There were no request failures, fallbacks, retries, or unexecuted turns. There is no independent accuracy or readiness score.

Raw first responses are under `responses/local/` and `responses/sol/`, one file per turn. The 72-row `grades.csv` has separate evidence, meaning, response, source, and context fields. Read targeted cases in batches consistent with the user's data limits. The saved `run.py` refuses to overwrite metadata or repeat paid calls.

The user authorized using the key from the separate checkout's `.env` in memory for this run; no key was copied or file in `main` modified.

The set is newly authored after prior exposure to records and regression work. Cases used for repairs become development/regression cases. Final release needs another unseen scenario set after fixes. Cunning is excluded; other editions and missing event text are handled as explicit scope boundaries rather than guessed rules.
